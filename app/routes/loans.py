from fastapi import APIRouter, HTTPException
from app.schemas.loan import LoanCreate, Loan
from app.database import get_db_connection
from typing import List, Optional
import mysql.connector
from datetime import datetime

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

@router.post("/", response_model=Loan)
def create_loan(loan: LoanCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    INSERT INTO loans (
        first_name, last_name, ssn, date_of_birth, address, city, state, zip_code,
        home_phone, mobile_phone, email, mobile_carrier, mother_maiden_name,
        housing_status, monthly_rent, years_at_current_address, requested_amount, 
        loan_purpose, employer_name, job_title, work_address, work_city, 
        work_state, work_zip_code, work_phone, years_at_current_job, gross_income, 
        pay_frequency, other_income, other_income_source, bank_name, account_type, 
        account_number, routing_number, months_with_bank,
        reference1_name, reference1_phone, reference1_relation,
        reference2_name, reference2_phone, reference2_relation,
        has_vehicle, vehicle_make, vehicle_model, vehicle_year,
        has_cosigner, cosigner_name, cosigner_phone, notes, status
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    """
    
    values = (
        loan.first_name, loan.last_name, loan.ssn, loan.date_of_birth, loan.address,
        loan.city, loan.state, loan.zip_code,
        loan.home_phone, loan.mobile_phone, loan.email, loan.mobile_carrier,
        loan.mother_maiden_name, loan.housing_status.value, loan.monthly_rent,
        loan.years_at_current_address, loan.requested_amount, loan.loan_purpose,
        loan.employer_name, loan.job_title, loan.work_address, loan.work_city,
        loan.work_state, loan.work_zip_code, loan.work_phone, loan.years_at_current_job, 
        loan.gross_income, loan.pay_frequency.value, loan.other_income, 
        loan.other_income_source, loan.bank_name, loan.account_type.value, 
        loan.account_number, loan.routing_number, loan.months_with_bank,
        loan.reference1_name, loan.reference1_phone, loan.reference1_relation,
        loan.reference2_name, loan.reference2_phone, loan.reference2_relation,
        loan.has_vehicle, loan.vehicle_make, loan.vehicle_model, loan.vehicle_year,
        loan.has_cosigner, loan.cosigner_name, loan.cosigner_phone, loan.notes,
        "Pending"  # Default status
    )
    try:
        cursor.execute(query, values)
        conn.commit()
        loan_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
        created_loan = cursor.fetchone()
        
        if created_loan.get("created_at"):
            created_loan["created_at"] = created_loan["created_at"].isoformat()
        if created_loan.get("updated_at"):
            created_loan["updated_at"] = created_loan["updated_at"].isoformat()
            
        return created_loan
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/", response_model=List[Loan])
def get_loans(status: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if status:
            if status not in ["Pending", "Approved", "Denied", "In Process"]:
                raise HTTPException(
                    status_code=400,
                    detail="Status must be: Pending, Approved, Denied or In Process"
                )
            cursor.execute(
                "SELECT * FROM loans WHERE status = %s ORDER BY created_at DESC", 
                (status,)
            )
        else:
            cursor.execute("SELECT * FROM loans ORDER BY created_at DESC")
        
        loans = cursor.fetchall()
        
        for loan in loans:
            if loan.get("created_at"):
                loan["created_at"] = loan["created_at"].isoformat()
            if loan.get("updated_at"):
                loan["updated_at"] = loan["updated_at"].isoformat()
                
        return loans
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()