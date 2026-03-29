from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.config.database import get_db
from server.db.models.element import Element
from server.db.models.project import Project
from server.api.v1.dependencies import get_current_user
from server.db.models.user import User
from server.db.models.element_type import ElementType
from server.schemas.element_type import ElementTypeResponse, ElementTypeCreate

router = APIRouter()

@router.get("/element_type/{element_id}", response_model=ElementTypeResponse)
async def get_element_type(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    
    result = await db.execute(
        select(Project).where(
            Project.id == element.project_id,
            Project.owner_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=403, detail="Access denied")
    
    result = await db.execute(select(ElementType).where(ElementType.id == element.element_type_id))
    element_type = result.scalar_one_or_none()

    if not element_type:
        raise HTTPException(status_code=404, detail="Тип элемента не найден")

    return element_type

@router.post("/upload_element_type", response_model=ElementTypeResponse)
async def upload(
    type: ElementTypeCreate,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_type = ElementType(
        title = type.title,
        length = type.length,
        width = type.width,
        zone_length = type.zone_length,
        zone_width = type.zone_width,
        description = type.description
    )

    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type
    

@router.get("/all_element_types", response_model=list[ElementTypeResponse])
async def get_element_types(
    db: AsyncSession = Depends(get_db)
):
    element_types = (await db.execute(select(ElementType))).scalars().all()

    return element_types