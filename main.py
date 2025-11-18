import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document
from schemas import Appointment, ContactMessage, DoctorProfile, Testimonial

app = FastAPI(title="Doctor Profile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Doctor Profile API is running"}

@app.get("/profile", response_model=DoctorProfile)
def get_doctor_profile():
    """Return static doctor profile content for the website hero/about sections"""
    profile = DoctorProfile(
        name="Dr. Amelia Hart",
        title="Board-Certified Cardiologist",
        location="San Francisco, CA",
        bio=(
            "Dr. Hart is a board-certified cardiologist with over 12 years of experience "
            "in preventative cardiology, heart failure management, and cardiac imaging. "
            "She believes in compassionate, evidence-based care tailored to each patient."
        ),
        specialties=["Preventive Cardiology", "Heart Failure", "Cardiac Imaging"],
        years_experience=12,
        education=[
            "MD, Johns Hopkins University School of Medicine",
            "Residency, Internal Medicine – UCSF Medical Center",
            "Fellowship, Cardiology – Stanford Health Care",
        ],
        certifications=["ABIM – Cardiovascular Disease", "ACLS/BLS"],
        languages=["English", "Spanish"],
        photo_url="/doctor.jpg",
        socials={
            "twitter": "https://twitter.com/doctor",
            "linkedin": "https://linkedin.com/in/doctor",
        },
    )
    return profile

@app.get("/testimonials", response_model=List[Testimonial])
def get_testimonials():
    return [
        Testimonial(name="Sofia M.", text="Dr. Hart took the time to listen and explained everything clearly.", rating=5),
        Testimonial(name="James R.", text="Truly expert care. I felt supported every step of the way.", rating=5),
        Testimonial(name="Priya K.", text="Super kind and thorough. Highly recommend!", rating=4),
    ]

@app.post("/appointments")
def request_appointment(payload: Appointment):
    try:
        doc_id = create_document("appointment", payload)
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
def send_contact_message(payload: ContactMessage):
    try:
        doc_id = create_document("contactmessage", payload)
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Basic environment/database check used by the tester page"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            import os as _os
            response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
