from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.config.database import get_db
from server.schemas.user import UserCreate, UserResponse, UserRequestDelete
from server.db.models.user import User
from server.api.v1.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse) 
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user

# Следует реализовать soft delete для финальной версии
@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: UserRequestDelete,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.verify_password(request.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid password")
    
    await db.delete(current_user)  
    await db.commit()
    return  
    

