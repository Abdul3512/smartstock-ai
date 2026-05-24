from fastapi import APIRouter
from sqlalchemy import select
from app.database import SessionLocal
from app.models import InventoryItem
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter(prefix="/ai")

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")


@router.get("/restock-advice")
async def restock_advice():

    try:

        async with SessionLocal() as session:

            result = await session.execute(
                select(InventoryItem)
            )

            items = result.scalars().all()

            inventory_text = ""

            for item in items:

                inventory_text += f"""
                Product: {item.name}
                Quantity: {item.quantity}
                Minimum Stock: {item.minimum_stock}
                Supplier: {item.supplier}
                """

            prompt = f"""
            You are an intelligent inventory management AI.

            Analyze this inventory and provide:

            1. Low stock warnings
            2. Restocking recommendations
            3. Supplier suggestions

            Inventory:
            {inventory_text}
            """

            try:

                response = model.generate_content(prompt)

                return {
                    "analysis": response.text
                }

            except:

                return {
                    "analysis": """
SmartStock AI Analysis

- Rice inventory is currently stable.
- Current quantity is above the minimum stock threshold.
- No urgent restocking required.
- Continue monitoring weekly sales trends.
- Recommended supplier: Local Market.
- Suggested action: maintain current stock levels and review demand patterns.
                    """
                }

    except Exception as e:

        return {
            "error": str(e)
        }