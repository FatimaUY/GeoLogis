from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
import logging

from ....services.taxe_fonciere_service import TaxeFonciereService
from ....repositories.taxe_fonciere_repository import TaxeFonciereRepository
from ....schemas.taxe_fonciere_schema import (
    TaxeFonciereCreateSchema,
    TaxeFonciereReadSchema,
    TaxeFonciereFilterSchema,
)
from ....model.database import engine, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/taxe_fonciere", tags=["taxe_fonciere"])

class SyncResponse(BaseModel):
    """Response model for sync operations."""
    success: bool
    message: str
    records_fetched: Optional[int] = None
    records_saved: Optional[int] = None
    fallback_count: Optional[int] = None
    duration_seconds: float

@router.post("/sync", response_model=SyncResponse)
async def sync_taxe_fonciere():
    """
    Trigger a synchronization of taxe foncière data.
    
    This endpoint fetches the latest taxe foncière data from the API
    and updates the database. The operation runs synchronously.
    
    Returns:
        SyncResponse: Status and summary of the synchronization operation
    """
    try:
        service = TaxeFonciereService()
        result = service.sync_taxe_fonciere_data()

        if result["success"]:
            return SyncResponse(
                success=True,
                message=result.get("message", "Sync completed successfully"),
                records_fetched=result.get("records_fetched"),
                records_saved=result.get("records_saved"),
                fallback_count=result.get("fallback_count"),
                duration_seconds=result.get("duration_seconds", 0),
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Sync failed for unknown reason"),
            )
    except Exception as e:
        logger.error(f"Error during API sync: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        )

@router.get("", response_model=List[TaxeFonciereReadSchema])
async def get_all_records(repo: TaxeFonciereRepository = Depends()):
    """Get all taxe foncière records."""
    try:
        return repo.get_all()
    except Exception as e:
        logger.error(f"Error fetching all records: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{record_id}", response_model=TaxeFonciereReadSchema)
async def get_record(record_id: int, repo: TaxeFonciereRepository = Depends()):
    """Get a specific taxe foncière record by ID."""
    try:
        record = repo.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching record {record_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-department/{dept}", response_model=List[TaxeFonciereReadSchema])
async def get_by_department(dept: str, repo: TaxeFonciereRepository = Depends()):
    """Get all records for a specific department."""
    try:
        return repo.get_by_dept(dept)
    except Exception as e:
        logger.error(f"Error fetching records for dept {dept}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-insee/{insee_com}", response_model=List[TaxeFonciereReadSchema])
async def get_by_insee(insee_com: str, repo: TaxeFonciereRepository = Depends()):
    """Get all records for a specific INSEE commune code."""
    try:
        return repo.get_by_insee(insee_com)
    except Exception as e:
        logger.error(f"Error fetching records for INSEE {insee_com}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-year/{annee_cible}", response_model=List[TaxeFonciereReadSchema])
async def get_by_year(annee_cible: int, repo: TaxeFonciereRepository = Depends()):
    """Get all records for a specific year."""
    try:
        return repo.get_by_year(annee_cible)
    except Exception as e:
        logger.error(f"Error fetching records for year {annee_cible}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-dept-year/{dept}/{annee_cible}", response_model=TaxeFonciereReadSchema)
async def get_by_dept_and_year(
    dept: str,
    annee_cible: int,
    repo: TaxeFonciereRepository = Depends()
):
    """Get a specific record for a department and year."""
    try:
        record = repo.get_by_dept_and_year(dept, annee_cible)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching record for {dept}/{annee_cible}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/fallback-count", response_model=int)
async def get_fallback_count(repo: TaxeFonciereRepository = Depends()):
    """Get count of records that used fallback years."""
    try:
        return repo.count_fallback()
    except Exception as e:
        logger.error(f"Error getting fallback count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/average-rates/{annee_cible}", response_model=dict)
async def get_average_rates(
    annee_cible: int,
    repo: TaxeFonciereRepository = Depends()
):
    """
    Get average tax rates for a specific year.
    
    Returns average values for:
    - taux_global_tfb: Built property tax
    - taux_global_tfnb: Land/unbuilt property tax
    - taux_plein_teom: Waste management tax
    - taux_global_th: Residence tax
    """
    try:
        result = repo.get_average_rates_by_year(annee_cible)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for year {annee_cible}"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating average rates for {annee_cible}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
