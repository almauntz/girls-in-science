from datetime import datetime, timedelta
from sqlmodel import Session
from app.database import engine
from app.models.profile import Workshop, WorkshopRegistration
from sqlmodel import Session, select, delete

with Session(engine) as db:
    # Prvo obriši stare podatke
    db.exec(delete(WorkshopRegistration))
    db.exec(delete(Workshop))
    db.commit()
    print("Stari podaci obrisani!")
    # Kreiraj radionice (u prošlosti da se pokažu kao završene)
    workshops = [
        Workshop(
            title="Python osnove",
            description="Uvod u Python programiranje za početnike.",
            date=datetime.utcnow() - timedelta(days=30),
            capacity=20
        ),
        Workshop(
            title="Git & GitHub",
            description="Osnove verzionisanja koda i timskog rada.",
            date=datetime.utcnow() - timedelta(days=14),
            capacity=15
        ),
        Workshop(
            title="Web dizajn s Tailwindom",
            description="Kako brzo izgraditi moderne UI komponente.",
            date=datetime.utcnow() - timedelta(days=7),
            capacity=20
        ),
    ]

    future_workshops = [
    Workshop(
        title="AI za početnike",
        description="Uvod u umjetnu inteligenciju i machine learning.",
        date=datetime.utcnow() + timedelta(days=5),
        capacity=25
    ),
    Workshop(
        title="Data Science s Pandasom", 
        description="Analiza podataka uz Python biblioteke.",
        date=datetime.utcnow() + timedelta(days=12),
        capacity=20
    ),
]


    for w in workshops:
        db.add(w)
    db.flush()  # da dobijemo ID-eve

    # Prijavi korisnika s ID=1 na sve radionice
    for w in workshops:
        db.add(WorkshopRegistration(user_id=1, workshop_id=w.id))


        for w in future_workshops:
            db.add(w)
        db.commit()


    print("Seed završen!")