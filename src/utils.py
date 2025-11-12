
import re
import json
import base64
import sqlite3
import os

import fitz
from typing import Dict, List, Optional, Any
from openai import OpenAI
from datetime import datetime
from src.models.receipt import Receipt


def extract_text_from_pdf(data_bytes: bytes):
    text = ""
    try:
        with fitz.open(stream=data_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

def extract_receipt_info(openai_client: OpenAI, data: bytes | str) -> Receipt:
    prompt = """
    Please extract the following information from this food delivery receipt and return it as a JSON object:

    {
        "platform": "name of the delivery platform (e.g., GoFood, GrabFood, Foodpanda)",
        "transaction_id": "transaction ID if available",
        "customer_name": "customer name if visible",
        "date": "transaction date in YYYY-MM-DD format",
        "time": "transaction time in HH:MM format",
        "restaurant": {
            "name": "restaurant name",
            "location": "restaurant location/address with full details including street, district, city"
        },
        "delivery": {
            "address": "full delivery address with street, district, city details",
            "fee": "delivery fee amount as number",
            "driver_name": "driver name if available",
            "driver_vehicle": "vehicle type and license plate if available",
            "distance": "delivery distance if available",
            "estimated_time": "estimated delivery time if available",
            "actual_delivery_time": "actual delivery time if available",
            "pickup_time": "pickup time from restaurant if available"
        },
        "items": [
            {
                "name": "item name",
                "quantity": "quantity as number",
                "unit_price": "individual unit price as number",
                "total_price": "total price for this item as number",
                "notes": "any special notes or modifications for this item"
            }
        ],
        "payment": {
            "subtotal": "subtotal/item total amount as number",
            "delivery_fee": "delivery fee as number",
            "service_fee": "service fee as number (if any)",
            "discount": "discount amount as number (if any)",
            "total": "total payment amount as number",
            "method": "payment method details (e.g., Credit Card, Cash, GoPay)",
        },
        "special_instructions": "any special instructions, notes, or environmental messages (e.g., no cutlery/straws)",
        "order_status": "delivery status information if available",
        "additional_info": {
            "thank_you_message": "any thank you or promotional messages",
            "environmental_note": "any environmental or sustainability messages",
            "final_note": "any additional notes or disclaimers at the bottom"
        }
    }

    Extract only the information that is clearly visible in the receipt. Use null for missing information.
    For numerical values, extract only the number without currency symbols and convert to IDR (Indonesian Rupiah).
    For example: if the receipt shows "Rp 69.000" or "69.000", extract as 69000.
    Pay special attention to:
    - Complete address details for both restaurant and delivery locations
    - Driver information and delivery logistics
    - Detailed breakdown of all fees and charges
    - Any special notes about environmental sustainability or special instructions
    - Exact timing information for pickup and delivery
    """
    
    try:
        # assert filename.split('.')[-1].lower() in ["png", "jpg", "jpeg", "pdf"], "data_type must be either 'image' or 'pdf'"
        # is_pdf = filename.lower().endswith(".pdf")

        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64.b64encode(data).decode('utf-8')}"
                            }
                        } if isinstance(data, bytes) else
                        {
                            "type": "text",
                            "text": data
                        },
                    ]
                }
            ],
            # max_completion_tokens=2000,
            # temperature=0,
        )
        
        # Extract the JSON from the response
        content = response.choices[0].message.content
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            receipt_data = json.loads(json_str)
        else:
            receipt_data = json.loads(content)
            
        # return receipt_data
        return Receipt.from_dict(receipt_data)
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return {"error": "Failed to parse receipt information", "raw_response": content}

    except Exception as e:
        print(f"Error extracting receipt information: {e}")
        return {"error": str(e)}
