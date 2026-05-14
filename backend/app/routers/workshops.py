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
@router.delete("/otkazivanje", status_code=status.HTTP_200_OK)
def otkazi_prijavu(radionica_id: int, email: str, db: Session = Depends(get_db)):
    # 1. Pronađi prijavu na osnovu emaila i ID-a radionice
    statement = select(Prijava).where(
        Prijava.radionica_id == radionica_id, 
        Prijava.email == email
    )
    rezultat = db.exec(statement).first()

    if not rezultat:
        raise HTTPException(status_code=404, detail="Prijava nije pronađena")

    # 2. Pronađi radionicu da vratiš mjesto (GT1-86)
    radionica = db.get(Workshop, radionica_id)
    if radionica:
        radionica.slobodna_mjesta += 1  # Oslobađanje mjesta
        db.add(radionica)

    # 3. Obriši prijavu iz baze
    db.delete(rezultat)
    db.commit()

    # 4. Poruka o uspješnoj odjavi (GT1-87)
    return {
        "status": "success", 
        "message": "Uspješno ste se odjavili sa radionice. Mjesto je oslobođeno."
    }