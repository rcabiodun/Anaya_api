from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from authentication.routes import auth_router
from config.database import  engine
from authentication.models import Base
from config.exceptions import DatabaseError, DuplicateEntryError, DatabaseConnectionError
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

port=os.getenv("PORT",8000)

app = FastAPI(
    title="Anaya API",
    # description="AN API description",
    version="1.0.0"
)

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(DuplicateEntryError)
async def duplicate_entry_handler(request: Request, exc: DuplicateEntryError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(DatabaseConnectionError)
async def connection_error_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
@app.on_event("startup")
async def startup_event():
    pass
    # create_tables()


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to your FastAPI application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,port=port)
