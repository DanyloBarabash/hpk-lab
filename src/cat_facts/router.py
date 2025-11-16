from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import get_db_session
from src.cat_facts.service import CatFactService
from src.cat_facts.models import (
    CatFactCreate,
    CatFactOut,
    CatFactStatsOut,
)

router = APIRouter(prefix="/facts", tags=["Cat Facts"])


def get_fact_service(session: AsyncSession = Depends(get_db_session)) -> CatFactService:
    return CatFactService(session)


@router.post("", response_model=CatFactOut)
async def create_fact(
    data: CatFactCreate,
    service: CatFactService = Depends(get_fact_service)
):
    """
    Create a new local cat fact.
    """
    try:
        return await service.create_fact(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/random")
async def get_fact(
    source: str = "local",
    service: CatFactService = Depends(get_fact_service)
):
    """
    Get a random cat fact.

    - source=local     → return local fact from DB + update stats
    - source=external  → return fact from external API
    """
    try:
        result = await service.get_fact(source)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fact_id}/stats", response_model=CatFactStatsOut)
async def get_fact_stats(
    fact_id: int,
    service: CatFactService = Depends(get_fact_service)
):
    """
    Return statistics for a specific local fact.
    """
    stats = await service.get_fact_stats(fact_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No statistics found for this fact")
    return stats


@router.get("", response_model=list[CatFactOut])
async def get_all_facts(
    service: CatFactService = Depends(get_fact_service)
):
    """
    Return all local cat facts.
    """
    try:
        facts = await service.fact_repo.get_all()
        return [CatFactOut.model_validate(f) for f in facts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{fact_id}")
async def delete_fact(
    fact_id: int,
    service: CatFactService = Depends(get_fact_service)
):
    """
    Delete a local cat fact and its statistics.
    """
    try:
        fact = await service.fact_repo.get_by_id(fact_id)
        if not fact:
            raise HTTPException(status_code=404, detail="Fact not found")

        await service.fact_repo.delete(fact_id)
        return {"status": "deleted", "id": fact_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
