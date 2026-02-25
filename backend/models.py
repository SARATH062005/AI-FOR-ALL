from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    skills = Column(String)  # Comma-separated or JSON string
    experience = Column(Text)
    education = Column(String)
    resume_path = Column(String)
    summary = Column(Text)
    recommendations = Column(Text)
    phone = Column(String)
    location = Column(String)
    github_url = Column(String)
    linkedin_url = Column(String)
    portfolio_url = Column(String)
    languages = Column(String)

    user = relationship("User", back_populates="profile")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    required_skills = Column(String)
    link = Column(String)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    platform = Column(String)
    link = Column(String)
    banner_url = Column(String)
    tags = Column(String)
