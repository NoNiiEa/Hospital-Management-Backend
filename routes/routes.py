from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status
from config.database import patients as patients_collection
from schema.patients_schemas import list_patient_schema
from .patients import patient_router
from .doctors import doctor_router
from .appointment import appointment_router
from .prescription import prescription_router
from .billing import billing_router
from .staff import router as staff_router
from .auth import router as auth_router, get_current_user

router = APIRouter()

router.include_router(patient_router, prefix="/patients", tags=["patients"])
router.include_router(doctor_router, prefix="/doctors", tags=["doctors"])
router.include_router(appointment_router, prefix="/appointments", tags=["appointments"])
router.include_router(prescription_router, prefix="/prescriptions", tags=["prescriptions"])
router.include_router(billing_router, prefix="/billings", tags=["billings"])
router.include_router(staff_router, prefix="/staffs", tags=["staffs"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return {"User": user}


