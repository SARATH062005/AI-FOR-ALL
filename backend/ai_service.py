import hmac
import json
import os
import requests
from typing import List, Dict

from dotenv import load_dotenv
load_dotenv()

import logging

# Configure logging to write to the same file
logging.basicConfig(
    filename='app_error.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_api_key_here")

def get_platform_logo(platform: str):
    """
    Returns a professional logo URL for common platforms.
    Using high-quality PNGs/SVGs from reliable sources.
    """
    logos = {
        "coursera": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-logo.png",
        "udemy": "https://www.vectorlogo.zone/logos/udemy/udemy-ar21.svg",
        "edx": "https://www.vectorlogo.zone/logos/edx/edx-ar21.svg",
        "linkedin": "https://www.vectorlogo.zone/logos/linkedin/linkedin-ar21.svg",
        "google": "https://www.vectorlogo.zone/logos/google/google-ar21.svg",
        "microsoft": "https://www.vectorlogo.zone/logos/microsoft/microsoft-ar21.svg",
        "youtube": "https://www.vectorlogo.zone/logos/youtube/youtube-ar21.svg",
        "khan academy": "https://www.vectorlogo.zone/logos/khanacademy/khanacademy-ar21.svg",
        "datacamp": "https://www.vectorlogo.zone/logos/datacamp/datacamp-ar21.svg",
        "pluralsight": "https://www.vectorlogo.zone/logos/pluralsight/pluralsight-ar21.svg"
    }
    p = platform.lower().strip()
    for key, url in logos.items():
        if key in p:
            return url
    return "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800"

def get_ai_recommendations(profile_data: Dict):
    """
    Get job and course recommendations based on profile data using OpenRouter.
    """
    prompt = f"""
    Based on the following user profile, suggest 5 relevant courses and 5 relevant jobs.
    Return the response in a strict JSON format with keys 'courses' and 'jobs'.
    Each course should have 'title', 'platform', 'link', 'banner_url', 'tags'.
    IMPORTANT: For 'banner_url', try to provide a relevant educational image or logo.
    Each job should have 'title', 'company', 'location', 'description', 'required_skills', 'link'.
    
    Profile:
    Full Name: {profile_data.get('full_name')}
    Skills: {profile_data.get('skills')}
    Experience: {profile_data.get('experience')}
    Education: {profile_data.get('education')}
    Summary: {profile_data.get('summary')}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-2.0-flash-001", # High speed, good for simple logic
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": { "type": "json_object" }
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Clean up JSON if AI adds markdown backticks
        content = content.strip()
        if "```" in content:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != 0:
                content = content[start:end]
        
        data = json.loads(content)
        
        # Validation and Formatting for Frontend
        if not data.get('courses') or not data.get('jobs'):
            print("DEBUG: AI returned empty lists, using fallback data")
            data = get_fallback_data()
            
        # Ensure tags and skills are strings and update logos
        for course in data.get('courses', []):
            if isinstance(course.get('tags'), list):
                course['tags'] = ", ".join(course['tags'])
            
            # Use real logos if platform is recognized
            course['banner_url'] = get_platform_logo(course.get('platform', ''))
        
        for job in data.get('jobs', []):
            if isinstance(job.get('required_skills'), list):
                job['required_skills'] = ", ".join(job['required_skills'])
                
        return data
    except Exception as e:
        logging.error(f"AI Recommendations Error: {e}", exc_info=True)
        print(f"AI Service Error: {e}")
        return get_fallback_data()

def get_fallback_data():
    return {
        "courses": [
            {"title": "Full Stack Web Development", "platform": "Coursera", "link": "https://coursera.org", "banner_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800", "tags": "React, Python, Tailwind"},
            {"title": "Mastering Robotics with ROS2", "platform": "Udemy", "link": "https://udemy.com", "banner_url": "https://images.unsplash.com/photo-1531746790731-6c087fecd05a?w=800", "tags": "ROS2, Robotics, Gazebo"},
            {"title": "AI & Machine Learning Foundations", "platform": "edX", "link": "https://edx.org", "banner_url": "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=800", "tags": "AI, ML, Python"}
        ],
        "jobs": [
            {"title": "Junior Robotics Engineer", "company": "Robotix Core", "location": "Bangalore", "description": "Help us build the next generation of warehouse robots. Experience with ROS2 is a plus.", "required_skills": "Python, ROS2, C++", "link": "#"},
            {"title": "Software Engineer Intern", "company": "Innovate AI", "location": "Remote", "description": "Contribute to cutting-edge AI projects in a fast-paced startup environment.", "required_skills": "Python, React, Fast API", "link": "#"},
            {"title": "Embedded Systems Intern", "company": "TechCircuit", "location": "Chennai", "description": "Design and test PCB layouts for IoT devices.", "required_skills": "PCB Design, Embedded C, Altium", "link": "#"}
        ]
    }

def parse_resume_to_profile(file_content: str):
    """
    Parse resume text to extract profile details using OpenRouter.
    """
    prompt = f"""
    Extract personal information from this resume text and return it in a strict JSON format with keys:
    'full_name', 'skills', 'experience', 'education', 'summary'.
    
    Resume Text:
    {file_content}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": { "type": "json_object" }
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        # Clean up JSON if AI adds markdown backticks
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"AI Service Error during parsing: {e}")
        return None
