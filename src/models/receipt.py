from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Restaurant:
    name: str
    location: Optional[str] = None


@dataclass
class Delivery:
    address: str
    fee: float
    driver_name: Optional[str] = None
    driver_vehicle: Optional[str] = None
    distance: Optional[str] = None
    estimated_time: Optional[str] = None
    actual_delivery_time: Optional[str] = None
    pickup_time: Optional[str] = None


@dataclass
class Item:
    name: str
    quantity: int
    unit_price: float
    total_price: Optional[float] = None
    notes: Optional[str] = None
    
    # Keep backward compatibility
    @property
    def price(self) -> float:
        """Backward compatibility - returns unit_price"""
        return self.unit_price


@dataclass
class Payment:
    subtotal: float
    delivery_fee: float
    service_fee: Optional[float] = None
    discount: float = 0.0
    total: float = 0.0
    method: str = ""


@dataclass
class AdditionalInfo:
    thank_you_message: Optional[str] = None
    environmental_note: Optional[str] = None
    final_note: Optional[str] = None


@dataclass
class Receipt:
    platform: str
    transaction_id: str
    date: str
    time: Optional[str]
    restaurant: Restaurant
    delivery: Delivery
    items: List[Item]
    payment: Payment
    customer_name: Optional[str] = None
    special_instructions: Optional[str] = None
    order_status: Optional[str] = None
    additional_info: Optional[AdditionalInfo] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Receipt':
        """Create Receipt instance from dictionary"""
        # Handle backward compatibility for items
        items_data = []
        for item in data.get('items', []):
            item_dict = {}
            if 'unit_price' in item:
                item_dict['unit_price'] = item['unit_price']
            elif 'price' in item:
                # Backward compatibility
                item_dict['unit_price'] = item['price']
            else:
                item_dict['unit_price'] = 0.0
                
            item_dict['name'] = item.get('name', '')
            item_dict['quantity'] = item.get('quantity', 1)
            item_dict['total_price'] = item.get('total_price')
            item_dict['notes'] = item.get('notes')
            items_data.append(item_dict)
        
        # Handle additional_info
        additional_info = None
        if 'additional_info' in data and data['additional_info']:
            additional_info = AdditionalInfo(**data['additional_info'])
        
        return cls(
            platform=data.get('platform', ''),
            transaction_id=data.get('transaction_id', ''),
            date=data.get('date', ''),
            time=data.get('time', ''),
            restaurant=Restaurant(**data.get('restaurant', {})),
            delivery=Delivery(**data.get('delivery', {})),
            items=[Item(**item) for item in items_data],
            payment=Payment(**data.get('payment', {})),
            customer_name=data.get('customer_name'),
            special_instructions=data.get('special_instructions'),
            order_status=data.get('order_status'),
            additional_info=additional_info
        )
    
    def to_dict(self) -> dict:
        """Convert Receipt instance to dictionary"""
        result = {
            'platform': self.platform,
            'transaction_id': self.transaction_id,
            'customer_name': self.customer_name,
            'date': self.date,
            'time': self.time,
            'restaurant': {
                'name': self.restaurant.name,
                'location': self.restaurant.location
            },
            'delivery': {
                'address': self.delivery.address,
                'fee': self.delivery.fee,
                'driver_name': self.delivery.driver_name,
                'driver_vehicle': self.delivery.driver_vehicle,
                'distance': self.delivery.distance,
                'estimated_time': self.delivery.estimated_time,
                'actual_delivery_time': self.delivery.actual_delivery_time,
                'pickup_time': self.delivery.pickup_time
            },
            'items': [
                {
                    'name': item.name,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'total_price': item.total_price,
                    'notes': item.notes
                } for item in self.items
            ],
            'payment': {
                'subtotal': self.payment.subtotal,
                'delivery_fee': self.payment.delivery_fee,
                'service_fee': self.payment.service_fee,
                'discount': self.payment.discount,
                'total': self.payment.total,
                'method': self.payment.method,
            },
            'special_instructions': self.special_instructions,
            'order_status': self.order_status
        }
        
        if self.additional_info:
            result['additional_info'] = {
                'thank_you_message': self.additional_info.thank_you_message,
                'environmental_note': self.additional_info.environmental_note,
                'final_note': self.additional_info.final_note
            }
        
        return result
    
    @property
    def datetime(self) -> datetime:
        """Get combined date and time as datetime object"""
        datetime_str = f"{self.date} {self.time}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    