from typing_extensions import Optional
from fastapi import HTTPException
from sqlmodel import Session, and_, select

from app.models.customer_dto import CustomerDTO
from app.models.customer import Customer
from app.models.transaction import Transaction

from app.schemas.customer_schema import CustomerSchema

from app.database.config import engine

session = Session(engine)

def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Customer) \
                .offset(skip) \
                .limit(limit))

def get_customer(db: Session, cutomer_id: int,
                page: int, size: int, initial_date: Optional[str],
                final_date: Optional[str], operator_name: Optional[str]):
    customer_dto = CustomerDTO(
        id=cutomer_id,
        name=None,
        page=page,
        size=size,
        initial_date=initial_date,
        final_date=final_date,
        operator_name=operator_name
    )

    if customer_dto.is_valid_operator_name_and_date():
        return _customer_by_operator_name_and_date(db, customer_dto)
    if customer_dto.is_valid_date():
        return _customer_by_date(db, customer_dto)
    if customer_dto.is_valid_operator_name():
        return _customer_by_operator_name(db, customer_dto)

def get_customer_from_id(db: Session, transaction_id: int):
    return session.exec(select(Customer).where(Customer.id == transaction_id)).first()


def create_account(db: Session, account: CustomerSchema):
    _account = Customer(name=account.name)

    db.add(_account)
    db.commit()
    db.refresh(_account)
    return _account


def remove_account(db: Session, account_id: int):
    _account = get_customer_from_id(db, account_id)

    db.delete(_account)
    db.commit()

def get_transfers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def _customer_exists(db: Session, account_id: int):
    return session.exec(select(Customer).where(Customer.id == account_id)).first() is not None

def _customer_by_operator_name_and_date(db: Session, customer_dto: CustomerDTO):
    if _customer_exists(db, customer_dto.id) is False:
        raise HTTPException(status_code=404, detail="Account not found")

    return session.exec(select(Transaction)\
        .where(and_(Transaction.account_id == customer_dto.id, \
        Transaction.operator_name == customer_dto.operator_name, \
        Transaction.date > customer_dto.initial_date, Transaction.date < customer_dto.final_date))\
        .offset(customer_dto.page).limit(customer_dto.size))


def _customer_by_date(db: Session, customer_dto: CustomerDTO):
    if _customer_exists(db, customer_dto.id) is False:
        raise HTTPException(status_code=404, detail="Account not found")

    return session.exec(select(Transaction) \
        .where(and_(Transaction.account_id == customer_dto.id, Transaction.date > customer_dto.initial_date, Transaction.date < customer_dto.final_date)) \
        .offset(customer_dto.page).limit(customer_dto.size))


def _customer_by_operator_name(db: Session, customer_dto: CustomerDTO):
    if _customer_exists(db, customer_dto.id) is False:
        raise HTTPException(status_code=404, detail="Account not found")

    return session.exec(select(Transaction) \
        .where(and_(Transaction.account_id == customer_dto.id, Transaction.operator_name == customer_dto.operator_name)) \
        .offset(customer_dto.page).limit(customer_dto.size))


def _customer_by_id(db: Session, customer_dto: CustomerDTO):
    if _customer_exists(db, customer_dto.id) is False:
        raise HTTPException(status_code=404, detail="Account not found")

    return session.exec(select(Transaction) \
        .where(Transaction.account_id == customer_dto.id) \
        .offset(customer_dto.page).limit(customer_dto.size))
