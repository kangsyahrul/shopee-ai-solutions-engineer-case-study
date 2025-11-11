
import re
import json
import base64
import sqlite3
import os

from typing import Dict, List, Optional, Any
from openai import OpenAI
from datetime import datetime
from src.models.receipt import Receipt


def extract_receipt_info(openai_client: OpenAI, image_bytes: bytes) -> Receipt:
    prompt = """
    Please extract the following information from this food delivery receipt image and return it as a JSON object:

    {
        "platform": "name of the delivery platform (e.g., GoFood, GrabFood, Foodpanda)",
        "transaction_id": "transaction ID if available",
        "date": "transaction date in YYYY-MM-DD format",
        "time": "transaction time in HH:MM format",
        "restaurant": {
            "name": "restaurant name",
            "location": "restaurant location/address"
        },
        "delivery": {
            "address": "delivery address",
            "fee": "delivery fee amount as number"
        },
        "items": [
            {
                "name": "item name",
                "quantity": "quantity as number",
                "price": "individual item price as number"
            }
        ],
        "payment": {
            "subtotal": "subtotal amount as number",
            "delivery_fee": "delivery fee as number",
            "service_fee": "service fee as number (if any)",
            "discount": "discount amount as number (if any)",
            "total": "total payment amount as number",
            "method": "payment method (e.g., Credit Card, Cash, E-wallet)"
        },
        "special_instructions": "any special instructions or notes"
    }

    Extract only the information that is clearly visible in the receipt. Use null for missing information.
    For numerical values, extract only the number without currency symbols and convert to IDR (Indonesian Rupiah).
    For example: if the receipt shows "Rp 69.000" or "69.000", extract as 69000.
    """
    
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
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
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0
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
