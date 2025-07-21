from fastapi import FastAPI
from app.routes.loans import router as loans_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Ultra Loans API",
    description="API para solicitudes de préstamos personales",
    version="1.0.0"
)

# Solo incluye el router de préstamos
app.include_router(loans_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Ultra Loans API"}