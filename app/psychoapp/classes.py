from dataclasses import dataclass


@dataclass
class PaymentInfo:
    psycho_name: str
    price: int
    amount_meets: int

