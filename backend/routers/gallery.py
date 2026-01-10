from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import User, TryOnImage
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/gallery")
async def gallery(username: str, request: Request, db: Session = Depends(get_db)):
    print(username)
    user = db.query(User).filter(
        User.username==username
    ).first()
    print("user: ", user)

    if not user:
        raise HTTPException(status_code=401, detail="You didn't logged In please login")
    
    gallery = []
    
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:8000"
    
    if user.role == 1:
        images = db.query(TryOnImage).all()

        usernames = dict()

        for img in images:
            if img.userid not in usernames:
                usernames[img.userid] = db.query(User).filter(User.id==user.id).first()

            username = usernames[img.userid].username

            gallery.append({
                "username": username,
                "person_image_url": f"{backend_url}/uploads{img.personimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
                "cloth_image_path": f"{backend_url}/uploads{img.clothimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
                "output_image_path": f"{backend_url}/uploads{img.outputimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
                "createdat":img.createdat
            })

        return gallery

    images = db.query(TryOnImage).filter(
        User.id==user.id, 
        TryOnImage.userid==user.id
    )

    for img in images:

        gallery.append({
            "username": user.username,
            "person_image_url": f"{backend_url}/uploads{img.personimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
            "cloth_image_path": f"{backend_url}/uploads{img.clothimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
            "output_image_path": f"{backend_url}/uploads{img.outputimagepath.replace('uploads','').replace('\\\\', '/').replace('\\', '/')}",
            "createdat":img.createdat
        })

    print(username)
    return {
        "status_code": 200,
        "detail": "Here your Gallery",
        "gallery": gallery
    }
