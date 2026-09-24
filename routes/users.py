from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from database import get_session

from models.user import User, UserCreate, UserRead

from auth import verify_api_key

router=APIRouter(
    prefix="/users",tags=["users"]
)

@router.post("/", response_model=UserRead)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # matching api key (Authentication)
    if api_key != "my_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")

    else:
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        user = User.model_validate(user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/", response_model=list[UserRead])
def list_users(
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
    ):

    if api_key != "my_secret_key":
            raise HTTPException(status_code=401, detail="Invalid API key")
    
    else:
        users = session.exec(select(User)).all()
        return users