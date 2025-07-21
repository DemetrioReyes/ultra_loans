from app.database import get_db_connection

def create_loans_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        ssn VARCHAR(11) NOT NULL,
        date_of_birth DATE NOT NULL,
        address TEXT NOT NULL,
        city VARCHAR(100) NOT NULL,
        state VARCHAR(50) NOT NULL,
        zip_code VARCHAR(10) NOT NULL,
        home_phone VARCHAR(15),
        mobile_phone VARCHAR(15) NOT NULL,
        email VARCHAR(100) NOT NULL,
        mobile_carrier VARCHAR(50) NOT NULL,
        mother_maiden_name VARCHAR(100) NOT NULL,
        housing_status ENUM('Rented', 'Owned', 'Living with Family', 'Other') NOT NULL,
        monthly_rent DECIMAL(10, 2),
        years_at_current_address INT,
        requested_amount DECIMAL(10, 2) NOT NULL,
        loan_purpose VARCHAR(255),
        employer_name VARCHAR(100) NOT NULL,
        job_title VARCHAR(100) NOT NULL,
        work_phone VARCHAR(15),
        work_address TEXT NOT NULL,
        years_at_current_job INT NOT NULL,
        gross_income DECIMAL(10, 2) NOT NULL,
        pay_frequency ENUM('Weekly', 'Bi-weekly', 'Monthly') NOT NULL,
        other_income DECIMAL(10, 2) DEFAULT 0.00,
        other_income_source VARCHAR(255),
        bank_name VARCHAR(100) NOT NULL,
        account_type ENUM('Savings', 'Checking') NOT NULL,
        account_number VARCHAR(20) NOT NULL,
        routing_number VARCHAR(20) NOT NULL,
        months_with_bank INT NOT NULL,
        reference1_name VARCHAR(100) NOT NULL,
        reference1_phone VARCHAR(15) NOT NULL,
        reference1_relation VARCHAR(50) NOT NULL,
        reference2_name VARCHAR(100) NOT NULL,
        reference2_phone VARCHAR(15) NOT NULL,
        reference2_relation VARCHAR(50) NOT NULL,
        has_vehicle BOOLEAN DEFAULT FALSE,
        vehicle_make VARCHAR(50),
        vehicle_model VARCHAR(50),
        vehicle_year INT,
        has_cosigner BOOLEAN DEFAULT FALSE,
        cosigner_name VARCHAR(100),
        cosigner_phone VARCHAR(15),
        status ENUM('Pending', 'Approved', 'Denied', 'In Process') DEFAULT 'Pending',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()