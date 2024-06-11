from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse

from sqlmodel import Session

from app.api.v1 import crud
from app.database.config import SessionLocal
from app.schemas.customer_schema import RequestCustomer
from app.schemas.api_schema import APIResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/index')
@router.get('/')
async def index():
    return {
        'message': 'Welcome to The Basic Bank API Example Project.',
        'success': True
    }

@router.get("/customers/all")
@router.get("/accounts/all")
async def get_all_account(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _accounts = crud.get_all_customers(db, skip, limit)
    return APIResponse(status="OK", code=200, message="Success", result=_accounts)

@router.get("/accounts")
async def get_account_by_id(
        id: int,
        page: int,
        size: int,
        initialDate: str | None = None,
        finalDate: str | None = None,
        operatorName: str | None = None,
        db: Session = Depends(get_db)
):
    _account = crud.get_customer(db, id, page, size, initialDate, finalDate, operatorName)
    _json_item = jsonable_encoder(_account)
    return JSONResponse(content=_json_item)



@router.post("/accounts")
async def create_account(request: RequestCustomer, db: Session = Depends(get_db)):
    _account = crud.create_account(db, account=request.parameter)
    return APIResponse(status="OK", code=200, message="Success", result=_account)


@router.get("/transfers")
async def get_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _transfer = crud.get_transfers(db, skip, limit)
    return APIResponse(status="OK", code=200, message="Success", result=_transfer)
