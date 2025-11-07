# routes/orders.py
from fastapi import APIRouter, HTTPException, Query
from models import OrderCreate, PaymentVerification, PaymentStatus
from services.midtrans_service import MidtransService
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Any
import uuid
import os
import logging

# ---------------------------------------------------------------------
# ENV & logger
# ---------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])
midtrans_service = MidtransService()

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
async def _attach_products_for_order(db, order: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tambahkan field 'products' ke order untuk kebutuhan email & Game Access.
    Sumber data: ebooks, minigames, exclusive_ebooks.
    Field diseragamkan:
      - product_type: 'ebook' | 'minigame' | 'ebook_exclusive'
      - file_url: file_url | driveDownloadLink
      - external_url: external_url | gameUrl
    """
    products: List[Dict[str, Any]] = []

    for it in order.get("items", []):
        ebook_id = (it or {}).get("ebookId")
        ptype = (it or {}).get("productType") or "ebook"
        if not ebook_id:
            continue

        doc = None
        # cari sesuai type dulu
        if ptype == "minigame":
            doc = await db.minigames.find_one({"id": ebook_id})
        elif ptype == "ebook_exclusive":
            doc = await db.exclusive_ebooks.find_one({"id": ebook_id})
        else:
            doc = await db.ebooks.find_one({"id": ebook_id})

        # fallback jika type tidak konsisten
        if not doc:
            doc = await db.ebooks.find_one({"id": ebook_id}) \
               or await db.minigames.find_one({"id": ebook_id}) \
               or await db.exclusive_ebooks.find_one({"id": ebook_id})

        if not doc:
            continue

        products.append({
            "id": doc.get("id"),
            "title": doc.get("title"),
            "product_type": ptype if ptype in ("ebook", "minigame", "ebook_exclusive")
                                 else ("minigame" if doc.get("external_url") or doc.get("gameUrl") else "ebook"),
            "file_url": doc.get("file_url") or doc.get("driveDownloadLink"),
            "external_url": doc.get("external_url") or doc.get("gameUrl"),
        })

    order["products"] = products
    return order


def _serialize_order(o: Dict[str, Any]) -> Dict[str, Any]:
    """Hapus _id dan serialize datetime → ISO agar aman dikirim ke client."""
    out = dict(o)
    out.pop("_id", None)
    for k in ("createdAt", "updatedAt", "paidAt"):
        if isinstance(out.get(k), datetime):
            out[k] = out[k].isoformat()
    return out


def _calculate_order_pricing(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Opsi bundling (bisa disesuaikan):
    - ebook: tiap 5 diskon 5.000
    - minigame: tiap 3 diskon 3.000
    - ebook_exclusive: tiap 4 diskon 25.000
    """
    subtotal = sum(it['price'] * it['quantity'] for it in items)
    by_type: Dict[str, int] = {}
    for it in items:
        t = it.get("productType", "ebook")
        by_type[t] = by_type.get(t, 0) + int(it.get("quantity", 1))

    discount = 0
    # ebook
    if by_type.get("ebook", 0) >= 5:
        discount += (by_type["ebook"] // 5) * 5000
    # minigame
    if by_type.get("minigame", 0) >= 3:
        discount += (by_type["minigame"] // 3) * 3000
    # ebook_exclusive
    if by_type.get("ebook_exclusive", 0) >= 4:
        discount += (by_type["ebook_exclusive"] // 4) * 25000

    total = max(0, subtotal - discount)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "bundleApplied": discount > 0,
    }

# ---------------------------------------------------------------------
# POST /orders/create
# ---------------------------------------------------------------------
@router.post("/create", response_model=dict)
async def create_order(order_data: OrderCreate):
    """
    Create order & initiate Midtrans payment (Snap).
    """
    from server import db

    try:
        # Ambil detail produk dari koleksi masing-masing
        order_items: List[Dict[str, Any]] = []

        for item in order_data.items:
            product_type = item.productType.value if hasattr(item.productType, 'value') else item.productType
            product = None

            if product_type == 'minigame':
                product = await db.minigames.find_one({"id": item.productId})
            elif product_type == 'ebook_exclusive':
                product = await db.exclusive_ebooks.find_one({"id": item.productId})
            else:
                product = await db.ebooks.find_one({"id": item.productId})

            if not product:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product {item.productId} not found in {product_type}"
                )

            order_items.append({
                "ebookId": item.productId,  # kompatibilitas lama
                "title": product.get("title"),
                "quantity": item.quantity,
                "price": product.get("price", 0),
                "productType": product_type,
                "driveDownloadLink": product.get("driveDownloadLink"),
                "gameUrl": product.get("gameUrl"),
            })

        # Harga (bundling optional)
        pricing = _calculate_order_pricing(order_items)

        # Buat ID order
        order_id = f"ORDER-{uuid.uuid4().hex[:10].upper()}"

        # Buat transaksi Midtrans
        midtrans_result = midtrans_service.create_transaction(
            order_id=order_id,
            customer_name=order_data.customerName,
            customer_email=order_data.customerEmail,
            items=order_items,
            to
