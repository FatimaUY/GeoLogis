from pydantic import BaseModel, Field
from typing import Optional


class PredictionInputSchema(BaseModel):
    """Schema for prediction input features."""
    
    annee: int = Field(ge=2020, le=2025)
    population: int = Field(ge=0)
    superficie_km2: float = Field(ge=0)
    zone_emploi: str
    taux_global_tfb: float = Field(ge=0)
    taux_global_tfnb: float = Field(ge=0)
    taux_plein_teom: float = Field(ge=0)
    taux_global_th: float = Field(ge=0)
    nb_ventes: int = Field(ge=0)
    densite: Optional[float] = Field(default=None, ge=0)
    ratio_taxe: Optional[float] = Field(default=None, ge=0)
    ventes_par_habitant: Optional[float] = Field(default=None, ge=0)
    taxe_x_population: Optional[float] = Field(default=None, ge=0)
    evolution_ventes: Optional[float] = None
    evolution_taxe: Optional[float] = None
    taxe_vs_moyenne_dep: Optional[float] = Field(default=None, ge=0)
    ventes_moyennes_dep: Optional[float] = Field(default=None, ge=0)
    dep_code: str
    reg_code: str
    code_postal: str

    class Config:
        from_attributes = True


class PredictionOutputSchema(BaseModel):
    """Schema for prediction output."""
    
    prediction: str = Field(description="Predicted class: 'hausse', 'baisse', or 'stable'")
    confidence: Optional[float] = Field(default=None, description="Prediction confidence score")
    features_used: int = Field(description="Number of features used in prediction")

    class Config:
        from_attributes = True


class ModelStatusSchema(BaseModel):
    """Schema for model training status."""
    
    is_trained: bool
    accuracy: Optional[float] = None
    total_training_samples: int = 0
    message: str

    class Config:
        from_attributes = True
