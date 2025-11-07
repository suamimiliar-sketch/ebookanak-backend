# routes/webhooks.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import os, json, hashlib

from server import db, logger  # db & logger dari server.py
from .email_service import send_order_email

router = APIRouter(prefix="/webhooks")

MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "")

def _midtrans_signature_valid(payload: dict) -> bool:
    """
    Verifikasi signature Midtrans sesuai dokumentasi:
    signature_key = SHA512(order_id + status_code + gross_amount + server_key)
    Catatan: gross_amount harus string apa adanya (tanpa koma).
    """
    try:
        provided = payload.get("signature_key", "")
        order_id = payload.get("order_id", "")
        status_code = payload.get("status_code", "")
        gross_amount = str(payload.get("gross_amount", ""))

        raw = (order_id or "") + (status_code or "") + (gross_amount or "") + MIDTRANS_SERVER_KEY
        calc = hashlib.sha512(raw.encode("utf-8")).hexdigest()
        return provided == calc
    except Exception:
        return False

async def _attach_products(order: dict) -> list[dict]:
    """Join produk (ebooks/minigames/exclusive_ebooks) untuk email & Game Access."""
    if not db or not order:
        return []

    out = []
    for it in order.get("items", []):
        ebook_id = (it or {}).get("ebook_id")
        if not ebook_id:
            continue

        p = await db.ebooks.find_one({"id": ebook_id})
        if not p:
            p = await db.minigames.find_one({"id": ebook_id})
        if not p:
            p = await db.exclusive_ebooks.find_one({"id": ebook_id})
        if not p:
            continue

        out.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "product_type": p.get("product_type") or ("minigame" if p.get("external_url") else "ebook"),
            "file_url": p.get("file_url"),
            "external_url": p.get("external_url"),
        })
    return out

@router.post("/midtrans")
async def midtrans_webhook(req: Request):
    """
    Terima notifikasi Midtrans. Saat status settlement/capture:
    - tandai order paid,
    - kirim email berisi link produk.
    """
    if not db:
        raise HTTPException(status_code=500, detail="db not initialized")

    body = await req.body()
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    order_id = payload.get("order_id")
    txn_status = payload.get("transaction_status")

    if not order_id:
        raise HTTPException(status_code=400, detail="order_id missing")

    # Signature optional: aktifkan jika ingin ketat & payload memiliki status_code/gross_amount
    if MIDTRANS_SERVER_KEY and payload.get("signature_key"):
        if not _midtrans_signature_valid(payload):
            raise HTTPException(status_code=401, detail="invalid signature")

    # Update status order
    new_status = "paid" if txn_status in ("settlement", "capture") else txn_status
    await db.orders.update_one(
        {"id": order_id},
        {"$set": {
            "status": new_status,
            "midtrans_payload": payload,
            "paid_at": datetime.utcnow() if new_status == "paid" else None,
            "updated_at": datetime.utcnow()
        }}
    )

    order = await db.orders.find_one({"id": order_id})
    if not order:
        return JSONResponse({"ok": True})

    # Join products untuk email
    products = await _attach_products(order)

    # Kirim email jika sudah paid
    if new_status == "paid":
        try:
            await send_order_email(to_email=order.get("email"), order=order, products=products)
        except Exception as e:
            logger.error(f"send_order_email failed: {e}")

    return JSONResponse({"ok": True})
