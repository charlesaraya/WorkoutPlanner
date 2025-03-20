from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import date
from enum import Enum

class EducationLevel(str, Enum):
    HIGH_SCHOOL = "High School"
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"
    CERTIFICATE = "Certificate"
    OTHER = "Other"

class EmploymentType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    FREELANCE = "Freelance"
    TEMPORARY = "Temporary"

class ContactInfo(BaseModel):
    phone: Optional[str] = Field(None, pattern = r"^\+?1?\d{9,15}$", description="Phone number in international format")
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None

class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    level: Optional[EducationLevel] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    location: Optional[str] = None
    relevant_coursework: Optional[List[str]] = None
    honors: Optional[List[str]] = None

class Certification(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

class WorkExperience(BaseModel):
    company: str
    position: str
    employment_type: Optional[EmploymentType] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = Field(None, description="None if current position")
    responsibilities: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    technologies: Optional[List[str]] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    technologies: Optional[List[str]] = None
    url: Optional[HttpUrl] = None

class Language(BaseModel):
    name: str
    proficiency: Optional[str] = Field(default=None, pattern=r"^(Native|Fluent|Advanced|Intermediate|Basic)$")

class Candidate(BaseModel):
    # Main information
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    contact_info: Optional[ContactInfo] = None

    # Work-related fields
    work_experience: Optional[List[WorkExperience]] = None
    total_years_experience: Optional[float] = Field(None, ge=0)
    current_employer: Optional[str] = None
    current_position: Optional[str] = None

    # Education
    education: Optional[List[Education]] = None
    highest_education_level: Optional[EducationLevel] = None

    # Skills and competencies
    technical_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None
    certifications: Optional[List[Certification]] = None

    # Projects and portfolio
    projects: Optional[List[Project]] = None

    # Additional information
    languages: Optional[List[Language]] = None
    awards: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    patents: Optional[List[str]] = None
