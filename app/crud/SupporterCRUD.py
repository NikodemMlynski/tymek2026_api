from app.schemas import supporter
from app.models import Supporter
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

class SupportersCRUD:
    @staticmethod
    def create_supporter(db: Session, supporter: supporter.SupporterIn):
        db_supporter = Supporter(
            name=supporter.name,
            class_=supporter.class_,
            approved=False
        )
        db.add(db_supporter)
        db.commit()
        db.refresh(db_supporter)
        return db_supporter

    def get_all_supporters(db: Session):
        return db.query(Supporter).filter(Supporter.approved == True).all()

    def get_supporters_count(db: Session):
        supporters_count = db.query(Supporter).filter(Supporter.approved == True).all()
        return {
            "count": len(supporters_count)
        }
    
    def get_not_approved_supporters(db: Session):
        return db.query(Supporter).filter(Supporter.approved == False).all()

    def approve_supported(db: Session, supporter_id: int, supporter_status: bool):
        supporter = db.query(Supporter).filter(Supporter.id == supporter_id).first()

        if not supporter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Supporter does not exist"
            )
        print(supporter_status)
        if supporter_status:
            supporter.approved = True 
            db.commit()
            return {
                "status": "Supporter approved"
            }
        else:
            db.delete(supporter)
            db.commit()
            return {
                "status": "Supporter deleted"
            }
        