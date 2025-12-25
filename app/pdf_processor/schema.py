from dataclasses import dataclass
from typing import List

@dataclass
class InvoiceItem:
    tid: str
    item_name: str
    qty: int
    rate: float
    amount: float

@dataclass
class Invoice:
    tid: str
    invoice_id: str
    issue_date: str
    total_due: float
    items: List[InvoiceItem]