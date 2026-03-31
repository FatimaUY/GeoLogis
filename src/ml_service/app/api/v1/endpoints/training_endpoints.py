from fastapi import APIRouter, Depends, Query
from ....services.training_service import TrainingService
from ....repositories.training_repository import TrainingRepository
from ....schemas.training_schema import TrainingCreateSchema, TrainingReadSchema
from ....model.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training", tags=["training"])

def get_training_service(db: Session = Depends(get_db)) -> TrainingService:
    return TrainingService(repo=TrainingRepository(db = db))

@router.get("/", response_model=TrainingReadSchema)
async def get_training_data(service: TrainingService = Depends(get_training_service)):
    return service.get_training_data()