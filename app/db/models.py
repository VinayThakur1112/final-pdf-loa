from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class InvoiceModel(Base):
    __tablename__ = "invoices"

    tid = Column(String, nullable=False)
    invoice_id = Column(String, primary_key=True)
    issue_date = Column(String)
    total_due = Column(String)

    items = relationship("InvoiceItemModel", back_populates="invoice")

class InvoiceItemModel(Base):
    __tablename__ = "invoice_items"

    tid = Column(String, nullable=False)
    id = Column(String, primary_key=True, autoincrement=True)
    invoice_id = Column(String, ForeignKey("invoices.invoice_id"))
    item_name = Column(String)
    qty = Column(String)
    rate = Column(String)
    amount = Column(String)

    invoice = relationship("InvoiceModel", back_populates="items")