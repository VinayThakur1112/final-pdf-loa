from app.db.session import SessionLocal
from app.db.models import InvoiceModel, InvoiceItemModel

def save_invoice(invoice):
    session = SessionLocal()

    try:
        inv = InvoiceModel(
            tid=invoice.tid,
            invoice_id=invoice.invoice_id,
            issue_date=invoice.issue_date,
            total_due=invoice.total_due,
        )

        session.add(inv)

        for item in invoice.items:
            session.add(
                InvoiceItemModel(
                    tid=invoice.tid,
                    invoice_id=invoice.invoice_id,
                    item_name=item.item_name,
                    qty=item.qty,
                    rate=item.rate,
                    amount=item.amount,
                )
            )

        session.commit()
        print("✅ Invoice saved to Cloud SQL")

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()