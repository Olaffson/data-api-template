from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from database.core import NotFoundError, get_db
from database.authentificate import oauth2_scheme, has_access, User
from database.sellers import Seller, SellerCreate, SellerUpdate, read_db_seller, read_db_one_seller, \
    create_db_seller, update_db_seller, delete_db_seller

PROTECTED = Annotated[User, Depends(has_access)]

router = APIRouter(
    prefix="/sellers",
)

@router.get("/{seller_id}", response_model=Seller)
def get_one_seller(request: Request, seller_id: str, db: Session = Depends(get_db)) -> Seller:
    try:
        db_seller = read_db_one_seller(seller_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Seller(**db_seller.__dict__)

@router.get("/", response_model=List[Seller])
def get_sellers(request: Request, db: Session = Depends(get_db)) -> List[Seller]:
    try:
        db_sellers = read_db_seller(db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return [Seller(**seller.__dict__) for seller in db_sellers]

@router.post("/")
def create_seller(has_access: PROTECTED, request: Request, seller: SellerCreate, db: Session = Depends(get_db)) -> Seller:
    db_seller = create_db_seller(seller, db)
    return Seller(**db_seller.__dict__)

@router.put("/{seller_id}")
def update_seller(has_access: PROTECTED, request: Request, seller_id: str, seller: SellerUpdate, db: Session = Depends(get_db)) -> Seller:
    try:
        db_seller = update_db_seller(seller_id, seller, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Seller(**db_seller.__dict__)

@router.delete("/{seller_id}")
def delete_seller(has_access: PROTECTED, request: Request, seller_id: str, db: Session = Depends(get_db)) -> Seller:
    try:
        db_seller = delete_db_seller(seller_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Seller(**db_seller.__dict__)
