from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import json

import models, schemas, auth, database, ai_service

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

import logging

# Configure logging to write to a file
logging.basicConfig(
    filename='app_error.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Internship Portal API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/profile", response_model=schemas.Profile)
async def create_profile(
    profile: schemas.ProfileCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
    else:
        db_profile = models.Profile(**profile.dict(), user_id=current_user.id)
        db.add(db_profile)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.post("/profile/resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with resume path
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not db_profile:
        db_profile = models.Profile(user_id=current_user.id, full_name=current_user.username, skills="", experience="", education="")
        db.add(db_profile)
    
@app.post("/profile", response_model=schemas.Profile)
async def create_or_update_profile(
    profile: schemas.ProfileCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    
    if db_profile:
        db_profile.full_name = profile.full_name
        db_profile.skills = profile.skills
        db_profile.experience = profile.experience
        db_profile.education = profile.education
        db_profile.summary = profile.summary
        db_profile.phone = profile.phone
        db_profile.location = profile.location
        db_profile.github_url = profile.github_url
        db_profile.linkedin_url = profile.linkedin_url
        db_profile.portfolio_url = profile.portfolio_url
        db_profile.languages = profile.languages
        db_profile.recommendations = None # Clear cache on update
    else:
        db_profile = models.Profile(
            user_id=current_user.id,
            **profile.dict()
        )
        db.add(db_profile)
    
    try:
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        db.rollback()
        logging.error(f"Error saving profile: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Could not save profile")

@app.post("/profile/resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Keep the folder structure for future use
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with resume path
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not db_profile:
        db_profile = models.Profile(user_id=current_user.id, full_name=current_user.username, skills="", experience="", education="")
        db.add(db_profile)
    
    db_profile.resume_path = file_path
    db_profile.recommendations = None # Clear cache on resume update
    db.commit()
    return {"message": "Resume uploaded successfully"}

@app.get("/recommendations")
async def get_recommendations(
    refresh: bool = False,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    print(f"DEBUG: Recommendation request for user_id={current_user.id} ({current_user.username}). Profile exists? {db_profile is not None}")
    if not db_profile:
        return {"courses": [], "jobs": []}
    
    # Check if we have cached recommendations (only if refresh is not requested)
    if not refresh and db_profile.recommendations:
        try:
            print(f"DEBUG: Returning cached recommendations for user {current_user.username}")
            return json.loads(db_profile.recommendations)
        except Exception as e:
            print(f"DEBUG: Failed to parse cached recommendations: {e}")
            # Continue to fetch from AI if cache is corrupted
            
    print(f"DEBUG: Generating fresh recommendations for user {current_user.username}")
    profile_data = {
        "full_name": db_profile.full_name,
        "skills": db_profile.skills,
        "experience": db_profile.experience,
        "education": db_profile.education,
        "summary": db_profile.summary
    }
    
    try:
        recommendations = ai_service.get_ai_recommendations(profile_data)
        # Save to cache
        db_profile.recommendations = json.dumps(recommendations)
        db.commit()
        
        print(f"DEBUG: Recommendations generated and cached: {len(recommendations.get('courses', []))} courses, {len(recommendations.get('jobs', []))} jobs")
        return recommendations
    except Exception as e:
        print(f"DEBUG: Recommendations failed: {e}")
        logging.error(f"Recommendations endpoint failed: {e}", exc_info=True)
        # Fallback within the endpoint just in case
        return {"courses": [], "jobs": []}

@app.get("/export/{format}")
async def export_data(
    format: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    import pandas as pd
    from fastapi.responses import FileResponse
    
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    data = [{
        "username": current_user.username,
        "email": current_user.email,
        "full_name": db_profile.full_name,
        "skills": db_profile.skills,
        "experience": db_profile.experience,
        "education": db_profile.education,
        "summary": db_profile.summary
    }]
    
    df = pd.DataFrame(data)
    file_path = f"data/user_data_{current_user.id}.{format}"
    
    if format == "csv":
        df.to_csv(file_path, index=False)
    elif format == "json":
        df.to_json(file_path, orient="records")
    elif format == "xlsx":
        df.to_excel(file_path, index=False)
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
        
    return FileResponse(file_path, filename=f"exported_data.{format}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
