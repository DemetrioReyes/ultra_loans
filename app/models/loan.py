from app.database import get_db_connection

def create_loans_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        campaign_token VARCHAR(64) NOT NULL,
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
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (campaign_token) REFERENCES admin_users(campaign_token)
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def apply_for_loan(loan_data: dict, campaign_token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Agregar el campaign_token a los datos del préstamo
    loan_data['campaign_token'] = campaign_token
    
    # Crear la consulta SQL dinámicamente
    fields = ', '.join(loan_data.keys())
    placeholders = ', '.join(['%s'] * len(loan_data))
    
    query = f"INSERT INTO loans ({fields}) VALUES ({placeholders})"
    
    try:
        cursor.execute(query, list(loan_data.values()))
        conn.commit()
        loan_id = cursor.lastrowid
        
        # Obtener el préstamo recién creado
        cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
        new_loan = cursor.fetchone()
        
        return new_loan
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()