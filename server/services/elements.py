from sqlalchemy import select
from server.db.models.element import Element

def rectangles_intersect(x1, y1, w1, h1, x2, y2, w2, h2) -> bool:
    left1 = x1 - w1 / 2
    right1 = x1 + w1 / 2
    bottom1 = y1 - h1 / 2
    top1 = y1 + h1 / 2

    left2 = x2 - w2 / 2
    right2 = x2 + w2 / 2
    bottom2 = y2 - h2 / 2
    top2 = y2 + h2 / 2

    no_overlap = (
        right1 <= left2 or 
        right2 <= left1 or 
        top1 <= bottom2 or
        top2 <= bottom1     
    )
    
    return not no_overlap

def is_rectangle_inside(
    inner_x: float, inner_y: float, inner_w: float, inner_l: float,
    outer_w: float, outer_l: float
) -> bool:

    inner_left = inner_x - inner_w / 2
    inner_right = inner_x + inner_w / 2
    inner_bottom = inner_y - inner_l / 2
    inner_top = inner_y + inner_l / 2

    return (
        inner_left >= 0 and
        inner_right <= outer_w and
        inner_bottom >= 0 and
        inner_top <= outer_l
    )

class ElementService:
    @staticmethod
    async def check_element_overlap(db, x: int, y: int, width: int, length: int, project_id: int, element_id: int = None):
        result = await db.execute(select(Element).where(Element.project_id == project_id, Element.id != element_id))
        elements = result.scalars().all()
        for element in elements:
            if rectangles_intersect(
                x, y, width, length,
                element.x, element.y, element.width, element.length
            ):
                return True
        return False

    @staticmethod
    async def check_element_border(x: int, y: int, width: int, length: int, project_width: int, project_length: int):
        return is_rectangle_inside(x, y, width, length, project_width, project_length)