from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from ..model.database import get_db
from ..model.training import Training
from ..schemas.training_schema import TrainingCreateSchema

class TrainingRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_training_data(self):
        return self.db.query(Training).all()
    
    def feed_data(self, data: TrainingCreateSchema):
        new_training_data = Training(**data.model_dump())
        self.db.add(new_training_data)
        self.db.commit()
        self.db.refresh(new_training_data)
        return new_training_data