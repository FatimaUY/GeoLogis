from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List

from ....services.training_service import TrainingService
from ....repositories.training_repository import TrainingRepository
from ....repositories.real_estate_repository import RealEstateMktRepository
from ....repositories.communes_repository import CommuneRepository
from ....repositories.inflation_rate_repository import InflationRateRepository
from ....schemas.training_schema import TrainingCreateSchema, TrainingReadSchema
from ....schemas.real_estate_schema import RealEstateMktCreateSchema
from ....schemas.communes_schema import CommuneCreateSchema
from ....schemas.inflation_rate_schema import InflationRateCreateSchema
from ....model.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training", tags=["training"])

# Base data directory
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent.parent / "data-pipeline" / "merge" / "raw"

def convert_nan_to_none(row_dict: dict) -> dict:
    """Convert NaN values in a dictionary to None."""
    return {k: None if pd.isna(v) else v for k, v in row_dict.items()}

def get_training_service(db: Session = Depends(get_db)) -> TrainingService:
    return TrainingService(repo=TrainingRepository(db=db))

@router.get("/", response_model=TrainingReadSchema)
async def get_training_data(service: TrainingService = Depends(get_training_service)):
    return service.get_training_data()


@router.post("/load/real-estate")
async def load_real_estate_training_data(db: Session = Depends(get_db)):
    """Load real estate training data from CSVs (2020-2025)."""
    repo = RealEstateMktRepository(db=db)
    total_loaded = 0
    
    for year in range(2020, 2026):
        csv_file = BASE_DIR / f"csv_agg_{year}.csv"
        if not csv_file.exists():
            continue
        
        df = pd.read_csv(str(csv_file), sep=";")
        df = df.dropna(subset=["code_commune", "annee"])
        
        # Filter to only numeric code_commune values
        df["code_commune"] = pd.to_numeric(df["code_commune"], errors="coerce")
        df = df.dropna(subset=["code_commune"])
        
        records = [
            RealEstateMktCreateSchema(**convert_nan_to_none(row.to_dict()))
            for _, row in df.iterrows()
        ]
    
    return {"status": "success", "source": "real_estate"}


@router.post("/load/communes")
async def load_communes_training_data(db: Session = Depends(get_db)):
    """Load communes training data from CSV."""
    repo = CommuneRepository(db=db)
    csv_file = BASE_DIR / "csv_communes_all.csv"
    
    if not csv_file.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {csv_file}")
    
    df = pd.read_csv(str(csv_file), sep=";")
    
    required_cols = [
        "code_insee", "nom_standard", "annee", "code_postal",
        "dep_code", "dep_nom", "reg_code", "reg_nom",
        "population", "densite", "superficie_km2",
        "latitude_centre", "longitude_centre", "zone_emploi"
    ]
    available_cols = [col for col in required_cols if col in df.columns]
    df = df[available_cols]
    df = df.dropna(subset=["code_insee", "nom_standard", "annee"])
    
    records = [
        CommuneCreateSchema(**convert_nan_to_none(row.to_dict()))
        for _, row in df.iterrows()
    ]

    return {"status": "success", "source": "communes"}


@router.post("/load/inflation")
async def load_inflation_training_data(db: Session = Depends(get_db)):
    """Load inflation rate training data from CSV."""
    repo = InflationRateRepository(db=db)
    csv_file = BASE_DIR / "inflation_rates.csv"
    
    if not csv_file.exists():
        csv_file = BASE_DIR.parent.parent / "flatfiles" / "taux_inflation.csv"
    
    if not csv_file.exists():
        raise HTTPException(status_code=404, detail="Inflation rates CSV not found")
    
    df = pd.read_csv(str(csv_file))
    df = df.dropna(subset=["annee"])
    
    records = [
        InflationRateCreateSchema(**convert_nan_to_none(row.to_dict()))
        for _, row in df.iterrows()
    ]

    return {"status": "success", "source": "inflation"}


@router.post("/load/all")
async def load_all_training_data(db: Session = Depends(get_db)):
    """Load all training data from CSVs."""
    results = {}
    
    try:
        results["real_estate"] = await load_real_estate_training_data(db)
    except Exception as e:
        results["real_estate"] = {"status": "error", "error": str(e)}
    
    try:
        results["communes"] = await load_communes_training_data(db)
    except Exception as e:
        results["communes"] = {"status": "error", "error": str(e)}
    
    try:
        results["inflation"] = await load_inflation_training_data(db)
    except Exception as e:
        results["inflation"] = {"status": "error", "error": str(e)}
    
    return results
