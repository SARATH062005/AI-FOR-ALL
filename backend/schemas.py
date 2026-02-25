from pydantic import BaseModel
from typing import List, Optional

class ProfileBase(BaseModel):
    full_name: str
    skills: str
    experience: str
    education: str
    summary: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    languages: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int
    resume_path: Optional[str] = None
    recommendations: Optional[str] = None

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    profile: Optional[Profile] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Job(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    required_skills: str
    link: str

    class Config:
        orm_mode = True

class Course(BaseModel):
    id: int
    title: str
    platform: str
    link: str
    banner_url: str
    tags: str

    class Config:
        orm_mode = True
