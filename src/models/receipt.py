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


@dataclass
class Item:
    name: str
    quantity: int
    price: float


@dataclass
class Payment:
    subtotal: float
    delivery_fee: float
    service_fee: Optional[float]
    discount: float
    total: float
    method: str


@dataclass
class Receipt:
    platform: str
    transaction_id: str
    date: str
    time: str
    restaurant: Restaurant
    delivery: Delivery
    items: List[Item]
    payment: Payment
    special_instructions: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Receipt':
        """Create Receipt instance from dictionary"""
        return cls(
            platform=data['platform'],
            transaction_id=data['transaction_id'],
            date=data['date'],
            time=data['time'],
            restaurant=Restaurant(**data['restaurant']),
            delivery=Delivery(**data['delivery']),
            items=[Item(**item) for item in data['items']],
            payment=Payment(**data['payment']),
            special_instructions=data.get('special_instructions')
        )
    
    def to_dict(self) -> dict:
        """Convert Receipt instance to dictionary"""
        return {
            'platform': self.platform,
            'transaction_id': self.transaction_id,
            'date': self.date,
            'time': self.time,
            'restaurant': {
                'name': self.restaurant.name,
                'location': self.restaurant.location
            },
            'delivery': {
                'address': self.delivery.address,
                'fee': self.delivery.fee
            },
            'items': [
                {
                    'name': item.name,
                    'quantity': item.quantity,
                    'price': item.price
                } for item in self.items
            ],
            'payment': {
                'subtotal': self.payment.subtotal,
                'delivery_fee': self.payment.delivery_fee,
                'service_fee': self.payment.service_fee,
                'discount': self.payment.discount,
                'total': self.payment.total,
                'method': self.payment.method
            },
            'special_instructions': self.special_instructions
        }
    
    @property
    def datetime(self) -> datetime:
        """Get combined date and time as datetime object"""
        datetime_str = f"{self.date} {self.time}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    