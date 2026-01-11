from pathlib import Path
from models.tryon_images import SaveTryOnImage
from database import get_db
from schemas.user import TryOnImage, User
from database import SessionLocal

db = SessionLocal()

BASE_DIR = Path("uploads/users")

async def save_try_on_images(data: SaveTryOnImage):
    try:
        user = db.query(User).filter(
            User.username==data.username
        ).first()

        imageData = TryOnImage(
            userid=user.id,
            personimagepath="",
            clothimagepath="",
            outputimagepath=""
        )

        db.add(imageData)

        db.flush()
        
        image_id = imageData.id
        
        try_ondir = BASE_DIR / data.username / f"tryon_{image_id}"

        try_ondir.mkdir(parents=True, exist_ok=True)
        
        person_path = try_ondir / "person.jpg"
        cloth_path = try_ondir / "cloth.jpg"
        output_path = try_ondir / "output.png"

        with open(person_path, "wb") as f:
            f.write(data.person_bytes)
        
        with open(cloth_path, "wb") as f:
            f.write(data.cloth_bytes)

        with open(output_path, "wb") as f:
            f.write(data.output_bytes)

        imageData.personimagepath = str(person_path)
        imageData.clothimagepath = str(cloth_path)
        imageData.outputimagepath = str(output_path)

        db.commit()

        return "Images Successfully Saved"
    
    except Exception as e:
        db.rollback()
        return e