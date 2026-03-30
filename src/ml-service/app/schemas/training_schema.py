from pydantic import BaseModel, Field
from ..model.training import Prediction

class TrainingCreateSchema(BaseModel):
    
    annee: int = Field(gt=2020, allow_inf_nan=False)
    code_commune: int = Field()
    prix_m2: float = Field()
    nom_commune: str = Field(min_length=0)
    dep_code: int = Field()
    dep_nom: str = Field(min_length=0)
    reg_code: int = Field()
    reg_nom: str = Field(min_length=0)
    code_postal: int = Field()
    population: int = Field()
    superficie_km2: float = Field()
    zone_emploi: int = Field()
    taux_global_tfb: float = Field()
    taux_global_tfnb: float = Field()
    taux_plein_teom: float = Field()
    taux_global_th: float = Field()
    sales_numbers: int = Field()
    market_prediction: Prediction

class TrainingReadSchema(BaseModel):
    
    annee: int
    code_commune: int
    prix_m2: float
    nom_commune: str
    dep_code: int
    dep_nom: str
    reg_code: int
    reg_nom: str
    code_postal: int
    population: int
    superficie_km2: float
    zone_emploi: int
    taux_global_tfb: float
    taux_global_tfnb: float
    taux_plein_teom: float
    taux_global_th: float
    sales_numbers: int
    market_prediction: Prediction
