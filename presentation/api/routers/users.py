from fastapi import APIRouter, Depends, status
from application.use_case.use_case_regiter_user import RegisterUser, RegisterUserCommand
from presentation.api.deps import get_register_user
from presentation.api.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, use_case: RegisterUser = Depends(get_register_user)):
    return await use_case.execute(RegisterUserCommand(**body.model_dump()))