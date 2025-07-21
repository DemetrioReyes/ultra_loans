from enum import Enum
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class HousingStatus(str, Enum):
    RENTED = "Rented"
    OWNED = "Owned"
    LIVING_WITH_FAMILY = "Living with Family"
    OTHER = "Other"

class AccountType(str, Enum):
    SAVINGS = "Savings"
    CHECKING = "Checking"

class PayFrequency(str, Enum):
    WEEKLY = "Weekly"
    BIWEEKLY = "Bi-weekly"
    MONTHLY = "Monthly"

class LoanStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    DENIED = "Denied"
    IN_PROCESS = "In Process"

class LoanBase(BaseModel):
    # Personal Information
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    ssn: str = Field(..., min_length=9, max_length=11)  # Format: XXX-XX-XXXX or XXXXXXXXX
    date_of_birth: date
    address: str
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=50)
    zip_code: str = Field(..., max_length=10)
    home_phone: Optional[str] = Field(None, max_length=15)
    mobile_phone: str = Field(..., max_length=15)
    email: str = Field(..., max_length=100)
    mobile_carrier: str = Field(..., max_length=50)
    mother_maiden_name: str = Field(..., max_length=100)
    
    # Housing Information
    housing_status: HousingStatus
    monthly_rent: Optional[float] = None
    years_at_current_address: Optional[int] = None
    
    # Loan Information
    requested_amount: float = Field(..., gt=0)
    loan_purpose: Optional[str] = Field(None, max_length=255)
    
    # Employment Information
    employer_name: str = Field(..., max_length=100)
    job_title: str = Field(..., max_length=100)
    work_address: str
    work_city: str = Field(..., max_length=100)
    work_state: str = Field(..., max_length=50)
    work_zip_code: str = Field(..., max_length=10)
    work_phone: Optional[str] = Field(None, max_length=15)
    years_at_current_job: int
    gross_income: float = Field(..., gt=0)
    pay_frequency: PayFrequency
    other_income: Optional[float] = 0.00
    other_income_source: Optional[str] = Field(None, max_length=255)
    
    # Banking Information
    bank_name: str = Field(..., max_length=100)
    account_type: AccountType
    account_number: str = Field(..., max_length=20)
    routing_number: str = Field(..., max_length=20)
    months_with_bank: int
    
    # References
    reference1_name: str = Field(..., max_length=100)
    reference1_phone: str = Field(..., max_length=15)
    reference1_relation: str = Field(..., max_length=50)
    reference2_name: str = Field(..., max_length=100)
    reference2_phone: str = Field(..., max_length=15)
    reference2_relation: str = Field(..., max_length=50)
    
    # Vehicle Information
    has_vehicle: bool = False
    vehicle_make: Optional[str] = Field(None, max_length=50)
    vehicle_model: Optional[str] = Field(None, max_length=50)
    vehicle_year: Optional[int] = None
    
    # Co-signer Information
    has_cosigner: bool = False
    cosigner_name: Optional[str] = Field(None, max_length=100)
    cosigner_phone: Optional[str] = Field(None, max_length=15)
    
    # Additional Information
    notes: Optional[str] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    status: LoanStatus
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True