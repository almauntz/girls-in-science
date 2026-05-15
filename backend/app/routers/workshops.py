from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.workshops_models import Prijava, Workshop
from typing import List

router = APIRouter(prefix="/workshops", tags=["workshops"])

# --- POSTOJEĆA RUTA ZA PRIJAVU ---
@router.post("/prijava", status_code=status.HTTP_201_CREATED)
def prijavi_studenticu(podaci: Prijava, db: Session = Depends(get_db)):
    radionica = db.get(Workshop, podaci.radionica_id)
    if not radionica:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena")

    if radionica.slobodna_mjesta <= 0:
        raise HTTPException(status_code=400, detail="Nema više slobodnih mjesta")

    radionica.slobodna_mjesta -= 1
    db.add(radionica)
    db.add(podaci)
    db.commit()
    db.refresh(podaci)

    return {
        "status": "success",
        "message": "Prijava uspješna!",
        "podaci": podaci
    }

# --- NOVA RUTA ZA OTKAZIVANJE (GT1-22) ---
@router.delete("/otkazivanje/{prijava_id}")
def otkazi_prijavu(
    prijava_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Pronađi prijavu u bazi
    prijava = db.get(Prijava, prijava_id)
    if not prijava:
        raise HTTPException(status_code=404, detail="Prijava nije pronađena")

    # 2. Pronađi radionicu na koju se prijava odnosi
    radionica = db.get(Workshop, prijava.workshop_id)
    
    # 3. Oslobađanje mjesta (Task: Oslobađanje mjesta nakon odjave)
    if radionica:
        radionica.slobodna_mjesta += 1
        db.add(radionica)

    # 4. Obriši prijavu
    db.delete(prijava)
    db.commit()

    # 5. Task: Poruka o uspješnoj odjavi
    return {"message": "Uspješno ste se odjavili sa radionice. Mjesto je oslobođeno."}