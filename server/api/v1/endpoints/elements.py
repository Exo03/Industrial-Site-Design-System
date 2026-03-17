from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from server.config.database import get_db
from server.schemas.element import ElementCreate, ElementResponse, ElementMove, ElementResize, ElementRecolor, ElementRename
from server.db.models.project_member import ProjectMember
from server.db.models.element import Element
from server.db.models.project import Project
from server.api.v1.dependencies import get_current_user
from server.db.models.user import User

router = APIRouter()

@router.post("/add_element", response_model=ElementResponse)
async def add_element_to_project(
    element: ElementCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    new_element = Element(
        element_type_id=element.element_type_id,
        x=element.x,
        y=element.y,
        width=element.width,
        length=element.length,
        project_id=element.project_id,
        title = element.title,
        color = element.color
    )
        
    db.add(new_element)
    await db.commit()
    await db.refresh(new_element)
    return new_element

@router.get("/project/{project_id}/elements", response_model=list[ElementResponse])
async def get_project_elements(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Project).where(Project.id == project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
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
    
    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    await db.delete(element)  
    await db.commit()
    return

@router.put("/move_element", response_model=ElementResponse)
async def move_element(
    new_element: ElementMove,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == new_element.id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    
    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    element.x = new_element.x
    element.y = new_element.y

    await db.commit()
    await db.refresh(element)

    return element

@router.put("/resize_element", response_model=ElementResponse)
async def resize_element(
    new_size: ElementResize,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == new_size.id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    
    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    element.width = new_size.width
    element.length = new_size.length

    await db.commit()
    await db.refresh(element)

    return element

@router.get("/element/{element_id}", response_model=ElementResponse)
async def get_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")

    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return element

@router.put("/recolor_element", response_model=ElementResponse)
async def recolor_element(
    new_color: ElementRecolor,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == new_color.id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    
    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    element.color = new_color.color

    await db.commit()
    await db.refresh(element)

    return element

@router.put("/rename_element", response_model=ElementResponse)
async def rename_element(
    new_title: ElementRename,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Element).where(Element.id == new_title.id))
    element = result.scalar_one_or_none()

    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    
    result = await db.execute(select(Project).where(Project.id == element.project_id,))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(select(ProjectMember).where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project.id
    ))
    member = result.scalar_one_or_none()

    if not member and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    element.title = new_title.title

    await db.commit()
    await db.refresh(element)

    return element
