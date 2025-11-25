from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.database import get_db
from schemas.project import ProjectCreate, ProjectResponse
from db.models.user import User
from db.models.project import Project
from api.v1.dependencies import get_current_user

router = APIRouter()

@router.post("/create_project", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )
    
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


@router.get("/user_projects", response_model=list[ProjectResponse])
async def get_user_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    projects = (await db.execute(
    select(Project).where(Project.owner_id == current_user.id)
    )).scalars().all()
    return projects

@router.delete("/delete_project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id  
        )
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    await db.delete(project)  
    await db.commit()
    return  

@router.put("/rename_project/{project_id}", response_model=ProjectResponse)
async def rename_project(
    project_id: int,
    new_project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
    )

    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    project.name = new_project.name
    project.description = new_project.description

    await db.commit()
    await db.refresh(project)
    return project