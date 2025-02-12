from bson import ObjectId

def individual_patient_schema(doctor):
    return {
        "id": str(doctor["_id"]),
        "name": doctor.get("name", "N/A"),
        "specialization": doctor.get("specialization", "N/A"),
        "contact": {
            "phone": doctor.get("contact", {}).get("phone", "N/A"),
            "email": doctor.get("contact", {}).get("email", "N/A"),
            "address": doctor.get("contact", {}).get("address", "N/A")
        },
        "schedule": [
            {
                "day": schedule.get("day", "N/A"),
                "timeslot": schedule.get("timeslot", "N/A")
            }
            for schedule in doctor.get("schedule", [])
        ],
        "patients": [
            {
                "patient_id": str(patient.get("patient_id", "N/A")),  
                "diagnosis": patient.get("diagnosis", "N/A"),
                "last_visit": str(patient.get("last_visit", "N/A")) 
            }
            for patient in doctor.get("patients", [])
        ]
    }

def list_doctor_schema(doctors):
    return [individual_patient_schema(doctor) for doctor in doctors]
