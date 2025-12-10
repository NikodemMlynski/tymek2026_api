from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.supporter import SupporterIn, SupporterOut, SupporterStatusIn
from app.database import get_db
from app.crud.SupporterCRUD import SupportersCRUD
from app.models import Supporter
from app.auth import verify_admin_code

router = APIRouter(prefix="/supporters", tags=["Supporters"])

@router.post("/")
def create_supporter(
    supporter_data: SupporterIn,
    db: Session = Depends(get_db)
):
    return SupportersCRUD.create_supporter(
        db=db,
        supporter=supporter_data
    )

@router.get("/")
def get_all_supporters(
    db: Session = Depends(get_db)
):
    return SupportersCRUD.get_all_supporters(db=db)

@router.get("/count")
def get_supporters_count(
    db: Session = Depends(get_db)
):
    return SupportersCRUD.get_supporters_count(db=db)

@router.get("/not_approved", dependencies=[Depends(verify_admin_code)])
def get_not_approved_supporters(
    db: Session = Depends(get_db)
):
    return SupportersCRUD.get_not_approved_supporters(db=db)

@router.put("/approve/{id}", dependencies=[Depends(verify_admin_code)])
def approve_supporter(
    id: int,
    status: SupporterStatusIn,
    db: Session = Depends(get_db)
):
    return SupportersCRUD.approve_supported(
        db=db,
        supporter_id=id,
        supporter_status=status.status
    )
