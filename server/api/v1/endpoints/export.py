from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.config.database import get_db
from server.db.models.user import User
from server.db.models.project import Project
from server.db.models.element import Element
from server.api.v1.dependencies import get_current_user
import svgwrite
import json
from weasyprint import HTML

router = APIRouter()

#добавлено с помощью ии
@router.get("/project/{project_id}/export/svg")
async def export_svg(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    project = await db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
    )
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден или доступ запрещён")

    elements = (await db.scalars(
        select(Element).where(Element.project_id == project_id)
    )).all()

    canvas_width = project.width
    canvas_height = project.length

    dwg = svgwrite.Drawing(size=(f"{canvas_width}px", f"{canvas_height}px"))

    dwg.add(dwg.rect(
        insert=(0, 0),
        size=(canvas_width, canvas_height),
        fill="white",
        stroke="#ccc",
        stroke_dasharray="4,4"
    ))

    for el in elements:
        dwg.add(dwg.rect(
            insert=(el.x, el.y),
            size=(el.width, el.length),
            fill=el.color or "#e0e0e0",
            stroke="#333333",
            stroke_width=1
        ))

        dwg.add(dwg.text(
            el.title,
            insert=(el.x + el.width / 2, el.y - 5),
            text_anchor="middle",
            font_family="Arial, sans-serif",
            font_size="12px",
            fill="#000000"
        ))

    return Response(
        content=dwg.tostring(),
        media_type="image/svg+xml",
        headers={
            "Content-Disposition": f'attachment; filename="project_{project_id}.svg"'
            }
        )

@router.get("/project/{project_id}/export/json", response_class=Response)
async def export_json(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    project = await db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
    )
    if not project:
        raise HTTPException(404, "Проект не найден или доступ запрещён")

    elements = (await db.scalars(
        select(Element).where(Element.project_id == project_id)
    )).all()

    result = {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "width": project.width,
            "length": project.length
        },
        "elements": [
            {
                "id": el.id,
                "element_type_id": el.element_type_id,
                "x": el.x,
                "y": el.y,
                "width": el.width,
                "length": el.length,
                "title": el.title,
                "color": el.color
            }
            for el in elements
        ]
    }

    return Response(
        content = json.dumps(result, ensure_ascii=False),#добавлено с помощью ии
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="project_{project_id}.json"'
        }
    )

@router.get("/project/{project_id}/export/pdf", response_class=Response)
async def export_pdf(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    project = await db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
    )
    if not project:
        raise HTTPException(404, "Проект не найден или доступ запрещён")

    elements = (await db.scalars(
        select(Element).where(Element.project_id == project_id)
    )).all()

    canvas_width = project.width
    canvas_height = project.length
    dwg = svgwrite.Drawing(size=(f"{canvas_width}px", f"{canvas_height}px"))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    for el in elements:
        dwg.add(dwg.rect(
            insert=(el.x, el.y),
            size=(el.width, el.length),
            fill=el.color or "#e0e0e0",
            stroke="#333333"
        ))
        dwg.add(dwg.text(   #добавлено с помощью ии
            el.title,
            insert=(el.x + el.width / 2, el.y - 5),
            text_anchor="middle",
            font_size="12px"
        ))

    svg_content = dwg.tostring()
    #добавлено с помощью ии
    html_content = f"""     
        <html>
        <head><meta charset="utf-8"/></head>
        <body style="margin: 0; padding: 0;">
            {svg_content}
        </body>
        </html>
        """
    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="project_{project_id}.pdf"'
        }
    )