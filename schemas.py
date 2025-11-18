"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- Appointment -> "appointment"
- ContactMessage -> "contactmessage"

These schemas are used for request/response validation and persistence.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Appointment(BaseModel):
    """
    Appointments requested by patients
    Collection: "appointment"
    """
    full_name: str = Field(..., description="Patient full name", min_length=2)
    email: EmailStr = Field(..., description="Patient email")
    phone: str = Field(..., description="Contact number", min_length=7)
    preferred_date: str = Field(..., description="Preferred appointment date (YYYY-MM-DD)")
    preferred_time: str = Field(..., description="Preferred time slot")
    service: str = Field(..., description="Requested service or reason for visit")
    notes: Optional[str] = Field(None, description="Additional notes")
    status: str = Field("pending", description="Status of request")

class ContactMessage(BaseModel):
    """
    Contact messages from site visitors
    Collection: "contactmessage"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)

class DoctorProfile(BaseModel):
    """
    Doctor public profile content (returned by API, not stored by default)
    """
    name: str
    title: str
    location: str
    bio: str
    specialties: List[str]
    years_experience: int
    education: List[str]
    certifications: List[str] = []
    languages: List[str] = ["English"]
    photo_url: Optional[str] = None
    socials: Optional[dict] = None

class Testimonial(BaseModel):
    name: str
    text: str
    rating: int = Field(ge=1, le=5)
    date: Optional[datetime] = None
