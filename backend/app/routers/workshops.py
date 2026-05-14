from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.workshops_models import Prijava, Workshop
router = APIRouter(prefix="/workshops", tags=["workshops"])

@router.post("/prijava", status_code=status.HTTP_201_CREATED) # GT1-98 i GT1-102
def prijavi_studenticu(podaci: Prijava, db: Session = Depends(get_db)):
    # 1. Pronađi radionicu da provjeriš mjesta (GT1-103)
    # Pretpostavljamo da imaš tabelu Workshop koja ima polje 'slobodna_mjesta'
    radionica = db.get(Workshop, podaci.radionica_id)
    
    if not radionica:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena")

    # Provjera da li ima slobodnih mjesta
    if radionica.slobodna_mjesta <= 0:
        raise HTTPException(status_code=400, detail="Nema više slobodnih mjesta")

    # 2. Smanji broj slobodnih mjesta (GT1-103)
    radionica.slobodna_mjesta -= 1
    db.add(radionica)

    # 3. Spremi prijavu u bazu (GT1-100)
    db.add(podaci)
    db.commit()
    db.refresh(podaci)

    # 4. Potvrda o uspješnoj prijavi (GT1-102)
    return {
        "status": "success",
        "message": "Prijava uspješna!",
        "podaci": podaci
    }