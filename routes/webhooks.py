# routes/webhooks.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Dict
import os, json, hashlib

from server import db, logger         # gunakan db & logger global dari server.py
from .email_service import send_order_email

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "")

def _midtrans_signature_valid(payload: dict) -> bool:
    """
    Midtrans: signature_key = SHA512(order_id + status_code + gross_amount + server_key)
    Beberapa notifikasi (test/sandbox) kadang tak menyertakan signature_key—kalau kosong, kita lewati.
    """
    provided = payload.get("signature_key")
    if not provided:
        return True  # longgarkan jika signature_key tidak ada
    order_id = payload.get("order_id", "")
    status_code = payload.get("status_code", "")
    gross_amount = str(payload.get("gross_amount", ""))
    raw = f"{order_id}{status_code}{gross_amount}{MIDTRANS_SERVER_KEY}"
    calc = hashlib.sha512(raw.encode("utf-8")).hexdigest()
    return provided == calc

async def _attach_products_for_order(order: dict) -> List[Dict]:
    """
    Join produk dari koleksi: ebooks, minigames, exclusive_ebooks.
    Map ke kunci seragam untuk email & Game Access:
      - product_type: 'ebook' | 'minigame' | 'ebook_exclusive'
      - file_url: file_url | driveDownloadLink
      - external_url: external_url | gameUrl
    """
    if not db or not order:
        return []
    out: List[Dict] = []
    for it in order.get("items", []):
        ebook_id = (it or {}).get("ebookId")
        ptype = (it or {}).get("productType") or "ebook"
        if not ebook_id:
            continue

        doc = None
        if ptype == "minigame":
            doc = await db.minigames.find_one({"id": ebook_id})
        elif ptype == "ebook_exclusive":
            doc = await db.exclusive_ebooks.find_one({"id": ebook_id})
        else:
            doc = await db.ebooks.find_one({"id": ebook_id})

        if not doc:
            # fallback: coba cari di koleksi lain jika type tidak konsisten
            doc = await db.ebooks.find_one({"id": ebook_id}) \
               or await db.minigames.find_one({"id": ebook_id}) \
               or await db.exclusive_ebooks.find_one({"id": ebook_id})

        if not doc:
            continue

        out.append({
            "id": doc.get("id"),
            "title": doc.get("title"),
            "product_type": ptype if ptype in ("ebook", "minigame", "ebook_exclusive")
                                 else ("minigame" if doc.get("external_url") or doc.get("gameUrl") else "ebook"),
            "file_url": doc.get("file_url") or doc.get("driveDownloadLink"),
            "external_url": doc.get("external_url") or doc.get("gameUrl"),
        })
    return out

@router.post("/midtrans")
async def midtrans_webhook(req: Request):
    """
    Terima notifikasi Midtrans. Saat status settlement/capture:
    - update order.paymentStatus = SUCCESS
    - set paidAt
    - kirim email link produk
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

    if MIDTRANS_SERVER_KEY and not _midtrans_signature_valid(payload):
        raise HTTPException(status_code=401, detail="invalid signature")

    # Map status Midtrans → status aplikasi
    new_status = "SUCCESS" if txn_status in ("settlement", "capture") else txn_status.upper()

    # Update order (berdasarkan orderId)
    await db.orders.update_one(
        {"orderId": order_id},
        {"$set": {
            "paymentStatus": new_status,
            "midtransPayload": payload,
            "paidAt": datetime.utcnow() if new_status == "SUCCESS" else None,
            "updatedAt": datetime.utcnow(),
        }}
    )

    order = await db.orders.find_one({"orderId": order_id})
    if not order:
        return JSONResponse({"ok": True})

    # Join products untuk email
    products = await _attach_products_for_order(order)

    # Kirim email hanya jika paid
    if new_status == "SUCCESS":
        try:
            await send_order_email(
                to_email=order.get("customerEmail"),
                order=order,
                products=products
            )
        except Exception as e:
            logger.error(f"send_order_email failed: {e}")

    return JSONResponse({"ok": True})
