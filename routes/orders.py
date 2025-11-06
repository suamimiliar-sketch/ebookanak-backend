from fastapi import APIRouter, HTTPException
from models import OrderCreate, OrderResponse, Order, PaymentVerification, OrderItem, PaymentStatus
from services.midtrans_service import MidtransService
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import uuid
import os
import logging

# Load environment variables before initializing services
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])
midtrans_service = MidtransService()


def calculate_order_pricing(items: list) -> dict:
    """
    Calculate order subtotal, discount, and total based on product type
    Bundle rules (same type only):
    - Ebooks: 5 for Rp 45,000 (Rp 5,000 discount)
    - Mini-games: 3 for Rp 12,000 (Rp 3,000 discount)
    - Ebooks Exclusive: 4 for Rp 175,000 (Rp 25,000 discount)
    """
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Group items by product type
    items_by_type = {}
    for item in items:
        product_type = item.get('productType', 'ebook')
        if product_type not in items_by_type:
            items_by_type[product_type] = []
        items_by_type[product_type].append(item)
    
    # Calculate discount per product type
    discount = 0
    
    for product_type, type_items in items_by_type.items():
        total_quantity = sum(item['quantity'] for item in type_items)
        
        if product_type == 'ebook':
            # Ebooks: every 5 = Rp 5,000 discount
            bundles = total_quantity // 5
            discount += bundles * 5000
        elif product_type == 'minigame':
            # Mini-games: every 3 = Rp 3,000 discount
            bundles = total_quantity // 3
            discount += bundles * 3000
        elif product_type == 'ebook_exclusive':
            # Ebooks Exclusive: every 4 = Rp 25,000 discount
            bundles = total_quantity // 4
            discount += bundles * 25000
    
    total = subtotal - discount
    
    return {
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'bundleApplied': discount > 0
    }


@router.post("/create", response_model=dict)
async def create_order(order_data: OrderCreate):
    """
    Create order and initiate Midtrans payment
    """
    from server import db
    
    try:
        # Fetch product details (ebooks, minigames, or ebook_exclusive)
        order_items = []
        
        for item in order_data.items:
            product_type = item.productType.value if hasattr(item.productType, 'value') else item.productType
            product = None
            
            # Fetch from appropriate collection based on product type
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
                'ebookId': item.productId,  # Keep as ebookId for backward compatibility
                'title': product['title'],
                'quantity': item.quantity,
                'price': product['price'],
                'productType': product_type,
                'driveDownloadLink': product.get('driveDownloadLink'),
                'gameUrl': product.get('gameUrl')  # For minigames
            })
        
        # Calculate pricing
        pricing = calculate_order_pricing(order_items)
        
        # Generate order ID
        order_id = f"ORDER-{uuid.uuid4().hex[:10].upper()}"
        
        # Create Midtrans transaction
        midtrans_result = midtrans_service.create_transaction(
            order_id=order_id,
            customer_name=order_data.customerName,
            customer_email=order_data.customerEmail,
            items=order_items,
            total=pricing['total'],
            discount=pricing['discount'],
            customer_phone=order_data.customerPhone
        )
        
        if not midtrans_result['success']:
            raise HTTPException(status_code=500, detail=f"Midtrans error: {midtrans_result.get('error')}")
        
        # Create order in database
        order = {
            'orderId': order_id,
            'customerEmail': order_data.customerEmail,
            'customerName': order_data.customerName,
            'customerPhone': order_data.customerPhone,  # Add customer phone
            'items': order_items,
            'subtotal': pricing['subtotal'],
            'discount': pricing['discount'],
            'total': pricing['total'],
            'bundleApplied': pricing['bundleApplied'],
            'paymentStatus': PaymentStatus.PENDING.value,
            'midtransOrderId': order_id,
            'snapToken': midtrans_result['token'],
            'notionDownloadLink': None,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        await db.orders.insert_one(order)
        
        return {
            'success': True,
            'data': {
                'orderId': order_id,
                'snapToken': midtrans_result['token'],
                'total': pricing['total'],
                'redirectUrl': midtrans_result['redirect_url']
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")


@router.get("/{order_id}")
async def get_order(order_id: str):
    """
    Get order details
    """
    from server import db
    
    try:
        order = await db.orders.find_one({"orderId": order_id})
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.pop('_id', None)
        return {
            'success': True,
            'data': order
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")


@router.post("/verify-payment")
async def verify_payment(verification: PaymentVerification):
    """
    Verify payment status after user completes payment
    """
    from server import db
    
    try:
        # Get transaction status from Midtrans
        status_result = midtrans_service.get_transaction_status(verification.orderId)
        
        if not status_result['success']:
            raise HTTPException(status_code=500, detail="Failed to verify payment")
        
        transaction_data = status_result['data']
        transaction_status = transaction_data.get('transaction_status')
        
        # Update order status
        payment_status = PaymentStatus.PENDING.value
        notion_link = None
        paid_at = None
        
        if transaction_status == 'settlement' or transaction_status == 'capture':
            payment_status = PaymentStatus.SUCCESS.value
            notion_link = os.environ.get('NOTION_DOWNLOAD_LINK', 'https://notion.so/pelangi-pintar-downloads')
            paid_at = datetime.utcnow()
        elif transaction_status in ['deny', 'expire', 'cancel']:
            payment_status = PaymentStatus.FAILED.value
        
        # Update order
        await db.orders.update_one(
            {"orderId": verification.orderId},
            {
                "$set": {
                    "paymentStatus": payment_status,
                    "notionDownloadLink": notion_link,
                    "midtransTransactionId": transaction_data.get('transaction_id'),
                    "paidAt": paid_at,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        
        return {
            'success': True,
            'data': {
                'paymentStatus': payment_status,
                'notionDownloadLink': notion_link
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to verify payment: {str(e)}")
