from ..repositories.training_repository import TrainingRepository
from ..schemas.training_schema import TrainingReadSchema, TrainingCreateSchema

class TrainingService:
    def __init__(self, repo = TrainingRepository):
        self.repo = repo
    
    def get_training_data(self):
        return self.repo.get_training_data()
    
    def add_data(self, training = TrainingCreateSchema):
        return self.repo.feed_data(training)