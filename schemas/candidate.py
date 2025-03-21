from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Optional, Dict
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
    phone: Optional[str] = Field(None, description="Candidate's phone number in international format")
    email: Optional[EmailStr] = Field(None, description="Candidate's primary email address")
    address: Optional[str] = Field(None, description="Candidate's physical mailing address")
    linkedin: Optional[HttpUrl] = Field(None, description="URL to the candidate's LinkedIn profile")
    github: Optional[HttpUrl] = Field(None, description="URL to the candidate's GitHub profile")
    portfolio: Optional[HttpUrl] = Field(None, description="URL to the candidate's portfolio website")
    website: Optional[HttpUrl] = Field(None, description="URL to the candidate's personal website")

class Education(BaseModel):
    institution: str = Field(..., description="Name of the educational institution")
    degree: Optional[str] = Field(None, description="Degree earned (e.g., Bachelor of Science)")
    level: Optional[EducationLevel] = Field(None, description="Level of education achieved")
    major: Optional[str] = Field(None, description="Primary field of study")
    minor: Optional[str] = Field(None, description="Secondary field of study")
    start_date: Optional[date] = Field(None, description="Date education began")
    end_date: Optional[date] = Field(None, description="Date education completed")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="Grade Point Average on 4.0 scale")
    location: Optional[str] = Field(None, description="City/State of the institution")
    relevant_coursework: Optional[List[str]] = Field(None, description="List of relevant courses taken")
    honors: Optional[List[str]] = Field(None, description="List of academic honors received")

class Certification(BaseModel):
    name: str = Field(..., description="Name of the certification")
    issuing_organization: Optional[str] = Field(None, description="Organization that issued the certification")
    issue_date: Optional[date] = Field(None, description="Date certification was issued")
    expiration_date: Optional[date] = Field(None, description="Date certification expires, if applicable")
    credential_id: Optional[str] = Field(None, description="Unique identifier for the certification")
    credential_url: Optional[HttpUrl] = Field(None, description="URL to verify the certification")

class WorkExperience(BaseModel):
    company: str = Field(..., description="Name of the employer")
    position: str = Field(..., description="Job title held")
    employment_type: Optional[EmploymentType] = Field(None, description="Type of employment")
    location: Optional[str] = Field(None, description="City/State of the workplace")
    start_date: Optional[date] = Field(None, description="Date employment began")
    end_date: Optional[date] = Field(None, description="Date employment ended, None if current")
    responsibilities: Optional[List[str]] = Field(None, description="List of job duties")
    achievements: Optional[List[str]] = Field(None, description="List of notable accomplishments")
    technologies: Optional[List[str]] = Field(None, description="Technologies used in the role")

class Project(BaseModel):
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(None, description="Brief description of the project")
    role: Optional[str] = Field(None, description="Candidate's role in the project")
    start_date: Optional[date] = Field(None, description="Date project began")
    end_date: Optional[date] = Field(None, description="Date project completed")
    technologies: Optional[List[str]] = Field(None, description="Technologies used in the project")
    url: Optional[HttpUrl] = Field(None, description="URL to project details or repository")

class Language(BaseModel):
    name: str = Field(..., description="Name of the language")
    proficiency: Optional[str] = Field(None, description="Proficiency level in the language")

class Candidate(BaseModel):
    first_name: str = Field(..., description="Candidate's first name")
    last_name: str = Field(..., description="Candidate's last name")
    middle_name: Optional[str] = Field(None, description="Candidate's middle name or initial")
    title: Optional[str] = Field(None, description="Professional title (e.g., Software Engineer)")
    summary: Optional[str] = Field(None, description="Brief professional summary")
    contact_info: Optional[ContactInfo] = Field(None, description="Candidate's contact information")

    work_experience: Optional[List[WorkExperience]] = Field(None, description="List of work experiences")
    total_years_experience: Optional[float] = Field(None, ge=0, description="Total years of professional experience")
    current_employer: Optional[str] = Field(None, description="Name of current employer")
    current_position: Optional[str] = Field(None, description="Current job title")

    education: Optional[List[Education]] = Field(None, description="List of educational experiences")
    highest_education_level: Optional[EducationLevel] = Field(None, description="Highest level of education achieved")

    technical_skills: Optional[List[str]] = Field(None, description="List of technical skills")
    soft_skills: Optional[List[str]] = Field(None, description="List of soft skills")
    certifications: Optional[List[Certification]] = Field(None, description="List of professional certifications")

    projects: Optional[List[Project]] = Field(None, description="List of personal or professional projects")

    languages: Optional[List[Language]] = Field(None, description="List of languages spoken")
    awards: Optional[List[str]] = Field(None, description="List of awards received")
    publications: Optional[List[str]] = Field(None, description="List of published works")
    patents: Optional[List[str]] = Field(None, description="List of patents held")
    volunteer_experience: Optional[List[WorkExperience]] = Field(None, description="List of volunteer experiences")
    professional_associations: Optional[List[str]] = Field(None, description="List of professional memberships")

    references: Optional[List[ContactInfo]] = Field(None, description="List of professional references")
    references_available: Optional[bool] = Field(None, description="Indicates if references are available upon request")