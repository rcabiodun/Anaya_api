from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

class DatabaseError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class DuplicateEntryError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)

class DatabaseConnectionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Database connection error. Please try again later."
        )