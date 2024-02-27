from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBSellers, NotFoundError
import string
import random

class Seller(BaseModel):
    seller_id: str
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str

class SellerCreate(BaseModel):
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str

class SellerUpdate(BaseModel):
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str

def read_db_one_seller(seller_id: str, session: Session) -> DBSellers:
    db_seller = session.query(DBSellers).filter(DBSellers.seller_id == seller_id).first()
    if db_seller is None:
        raise NotFoundError(f"Item with id {seller_id} not found.")
    return db_seller

def read_db_seller(session: Session) -> List[DBSellers]:
    db_seller = session.query(DBSellers).limit(5).all()
    if db_seller is None:
        raise NotFoundError("Database is empty")
    return db_seller

def generate_id() -> str:
    """Generate a unique string ID."""
    length = 14
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def create_db_seller(seller: SellerCreate, session: Session) -> DBSellers:
    db_seller = DBSellers(**seller.dict(), seller_id=generate_id())
    session.add(db_seller)
    session.commit()
    session.refresh(db_seller)
    return db_seller

def update_db_seller(seller_id: str, seller: SellerUpdate, session: Session) -> DBSellers:
    db_seller = read_db_one_seller(seller_id, session)
    for key, value in seller.dict().items():
        setattr(db_seller, key, value)
    session.commit()
    session.refresh(db_seller)
    return db_seller

def delete_db_seller(seller_id: str, session: Session) -> DBSellers:
    db_seller = read_db_one_seller(seller_id, session)
    session.delete(db_seller)
    session.commit()
    return db_seller
