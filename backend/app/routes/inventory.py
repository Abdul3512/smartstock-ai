from fastapi import APIRouter
from sqlalchemy import select
from app.database import SessionLocal
from app.models import InventoryItem

router = APIRouter(prefix="/inventory")

@router.post("/add")
async def add_item(item: dict):

    async with SessionLocal() as session:

        new_item = InventoryItem(
            name=item["name"],
            category=item["category"],
            quantity=item["quantity"],
            minimum_stock=item["minimum_stock"],
            supplier=item["supplier"]
        )

        session.add(new_item)

        await session.commit()

        return {"message": "Item added"}

@router.get("/")
async def get_items():

    async with SessionLocal() as session:

        result = await session.execute(
            select(InventoryItem)
        )

        items = result.scalars().all()

        return [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "quantity": item.quantity,
                "minimum_stock": item.minimum_stock,
                "supplier": item.supplier
            }
            for item in items
        ]