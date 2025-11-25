from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from config.database import get_db
from schemas.element import ElementCreate, ElementResponse, ElementUpdate
from db.models.element import Element
from db.models.project import Project
from api.v1.dependencies import get_current_user
from db.models.user import User

router = APIRouter()

@router.post("/add_element", response_model=ElementResponse)
async def add_element_to_project(
    element: ElementCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    project_result = await db.execute(
        select(Project).where(
            Project.id == element.project_id,
            Project.owner_id == current_user.id
        )
    )
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    try:
        new_element = Element(
            element_type_id=element.element_type_id,
            x=element.x,
            y=element.y,
            project_id=element.project_id,
            rotation=0
        )
        
        db.add(new_element)
        await db.commit()
        await db.refresh(new_element)
        return new_element
        
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Element with these coordinates already exists in this project"
        )

@router.get("/project/{project_id}/elements", response_model=list[ElementResponse])
async def get_project_elements(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    project_result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
    )
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    elements_result = await db.execute(
        select(Element).where(Element.project_id == project_id)
    )
    elements = elements_result.scalars().all()
    return elements

@router.delete("/delete_element/{element_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Element).where(Element.id == element_id)
    )
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
    
    await db.delete(element)  
    await db.commit()
    return

@router.put("/move_element/{element_id}", response_model=ElementResponse)
async def move_element(
    new_element: ElementUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == new_element.id))
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
    
    conflict_exists = await db.execute(
        select(exists().where(
            Element.project_id == element.project_id,
            Element.x == new_element.x,
            Element.y == new_element.y,
            Element.id != element.id
        ))
    )
    if conflict_exists.scalar():
        raise HTTPException(status_code=400, detail="В этом проекте уже есть элемент с такими координатами")

    element.x = new_element.x
    element.y = new_element.y
    element.rotation = new_element.rotation

    await db.commit()
    await db.refresh(element)
    return element