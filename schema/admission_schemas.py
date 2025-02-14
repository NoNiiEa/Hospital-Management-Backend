from bson import ObjectId

def individual_admission_schema(admission):
    return {
        "id": str(admission["_id"]),
        "patient": admission.get("patient_id","N/A"),
        "admission_date": admission.get("admission_date","N/A"),
        "expected_discharge_date": admission.get("expected_discharge_date", "N/A"),
        "actual_discharge_date": admission.get("actual_discharge_date", "N/A"),
        "doctor_id": admission.get("doctor_id", "N/A"),
        "department": admission.get("department", "N/A"),
        "admission_reason": admission.get("admission_reason", "N/A"),
        "ward": admission.get("ward", "N/A"),
        "bed_number": admission.get("bed_number", "N/A"),
        "status": admission.get("status", "N/A"),
        "treatment_plan": [{
            "procedure" :treatment_plan.get("procedure", "N/A"),
            "scheduled_date" :treatment_plan.get("scheduled_date", "N/A"),
            "status" :treatment_plan.get("status", "N/A")
            }for treatment_plan in admission.get("treatment_plan", [])
        ],
        "medications": [{
            "name" :medications.get("name", "N/A"),
            "dosage" :medications.get("dosage", "N/A"),
            "frequency" :medications.get("frequency", "N/A"),
            "duration" :medications.get("duration", "N/A")
            }for medications in admission.get("treatment_plan", [])
        ],

        
        
    }

def list_admission_schema(admissions):
    return [individual_admission_schema(admission) for admission in admissions]
'''
class AdmissionModel(BaseModel):
        patient_id: str
        admission_date = str
        expected_discharge_date = str
        actual_discharge_date = str
        doctor_id = str
        department = str
        admission_reason = str
        ward =str
        bed_number = str
        status = str
        treatment_plan = [TreatmentModel]
        medications = [MedicationModel]
'''