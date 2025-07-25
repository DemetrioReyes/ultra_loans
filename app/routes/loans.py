from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.loan import apply_for_loan

router = APIRouter(prefix="/loans", tags=["loans"])

class LoanApplication(BaseModel):
    first_name: str
    last_name: str
    ssn: str
    date_of_birth: str
    address: str
    city: str
    state: str
    zip_code: str
    mobile_phone: str
    email: str
    mobile_carrier: str
    mother_maiden_name: str
    housing_status: str
    requested_amount: float
    employer_name: str
    job_title: str
    work_address: str
    work_city: str
    work_state: str
    work_zip_code: str
    years_at_current_job: int
    gross_income: float
    pay_frequency: str
    bank_name: str
    account_type: str
    account_number: str
    routing_number: str
    months_with_bank: int
    reference1_name: str
    reference1_phone: str
    reference1_relation: str
    reference2_name: str
    reference2_phone: str
    reference2_relation: str
    monthly_rent: Optional[float] = None
    years_at_current_address: Optional[int] = None
    loan_purpose: Optional[str] = None
    work_phone: Optional[str] = None
    other_income: Optional[float] = 0.0
    other_income_source: Optional[str] = None
    has_vehicle: Optional[bool] = False
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    has_cosigner: Optional[bool] = False
    cosigner_name: Optional[str] = None
    cosigner_phone: Optional[str] = None

@router.post("/apply/{campaign_token}")
async def create_loan_application(
    campaign_token: str,
    loan: LoanApplication
):
    try:
        # Convertir la fecha de nacimiento a formato MySQL
        date_of_birth = datetime.strptime(loan.date_of_birth, "%Y-%m-%d").date()
        
        # Crear el diccionario con los datos del préstamo
        loan_data = loan.model_dump()
        loan_data["date_of_birth"] = date_of_birth
        
        # Eliminar los valores None del diccionario
        loan_data = {k: v for k, v in loan_data.items() if v is not None}
        
        # Aplicar para el préstamo
        new_loan = apply_for_loan(loan_data, campaign_token)
        return new_loan
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )