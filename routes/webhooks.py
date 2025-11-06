from fastapi import APIRouter, Request, HTTPException
from services.midtrans_service import MidtransService
from services.notification_service import send_order_notifications
from models import PaymentStatus
from datetime import datetime, timedelta, timezone
import uuid
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
midtrans_service = MidtransService()


@router.post("/test-midtrans")
async def test_midtrans_webhook(request: Request):
    """
    Test endpoint to simulate Midtrans webhook - NO signature verification
    Use this to test webhook processing without requiring real Midtrans data
    """
    from server import db
    
    try:
        data = await request.json()
        logger.info(f"TEST WEBHOOK - Received data: {data}")
        
        order_id = data.get('order_id')
        transaction_status = data.get('transaction_status', 'settlement')
        transaction_id = data.get('transaction_id', f"test-txn-{uuid.uuid4()}")
        payment_type = data.get('payment_type', 'bank_transfer')
        gross_amount = data.get('gross_amount', '10000')
        
        # For testing, always mark as SUCCESS
        payment_status = PaymentStatus.SUCCESS.value
        notion_link = os.environ.get('NOTION_DOWNLOAD_LINK', 'https://notion.so/pelangi-pintar-downloads')
        now_utc = datetime.now(timezone.utc)
        paid_at = now_utc.isoformat()
        
        # Update order
        update_result = await db.orders.update_one(
            {"orderId": order_id},
            {
                "$set": {
                    "paymentStatus": payment_status,
                    "notionDownloadLink": notion_link,
                    "midtransTransactionId": transaction_id,
                    "paidAt": paid_at,
                    "updatedAt": now_utc.isoformat()
                }
            }
        )
        
        if update_result.modified_count == 0:
            return {
                'success': False,
                'message': f'Order {order_id} not found in database'
            }
        
        logger.info(f"TEST WEBHOOK - Order {order_id} updated successfully")
        
        # Get order for notifications
        order = await db.orders.find_one({"orderId": order_id})
        if order:
            ebooks = []
            games = []
            
            for item in order.get('items', []):
                product_type = item.get('productType', 'ebook')
                
                if product_type == 'minigame':
                    games.append({
                        'id': item.get('ebookId'),
                        'title': item.get('title'),
                        'quantity': item.get('quantity', 1)
                    })
                elif item.get('driveDownloadLink'):
                    ebooks.append({
                        'title': item['title'],
                        'downloadLink': item['driveDownloadLink'],
                        'thumbnail': item.get('thumbnailUrl', ''),
                        'description': item.get('description', ''),
                        'quantity': item.get('quantity', 1)
                    })
            
            # Try to send notifications
            notification_status = {
                'ebooks_sent': False,
                'games_sent': False
            }
            
            if ebooks:
                try:
                    notification_results = send_order_notifications(
                        customer_email=order.get('customerEmail'),
                        customer_name=order.get('customerName'),
                        customer_phone=order.get('customerPhone', ''),
                        order_id=order_id,
                        ebooks=ebooks
                    )
                    notification_status['ebooks_sent'] = notification_results.get('email_sent', False)
                    logger.info(f"TEST WEBHOOK - Ebook notifications: {notification_results}")
                except Exception as e:
                    logger.error(f"TEST WEBHOOK - Failed to send ebook notifications: {str(e)}")
            
            if games:
                try:
                    from services.notification_service import send_game_links_email
                    
                    game_details = []
                    for game in games:
                        game_data = await db.minigames.find_one({"id": game['id']})
                        if game_data:
                            token_id = str(uuid.uuid4())
                            expires_at = now_utc + timedelta(hours=24)
                            
                            access_token_doc = {
                                "tokenId": token_id,
                                "orderId": order_id,
                                "gameId": game['id'],
                                "customerEmail": order.get('customerEmail'),
                                "customerName": order.get('customerName'),
                                "gameUrl": game_data.get('gameUrl'),
                                "createdAt": now_utc.isoformat(),
                                "expiresAt": expires_at.isoformat(),
                                "isActive": True,
                                "accessCount": 0
                            }
                            
                            await db.game_access_tokens.insert_one(access_token_doc)
                            
                            frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
                            proxy_url = f"{frontend_url}/api/game-access/{token_id}"
                            
                            game_details.append({
                                'id': game['id'],
                                'title': game_data.get('title'),
                                'gameUrl': proxy_url,
                                'icon': game_data.get('icon', '🎮'),
                                'thumbnail': game_data.get('thumbnailUrl', ''),
                                'description': game_data.get('description', ''),
                                'quantity': game.get('quantity', 1)
                            })
                    
                    if game_details:
                        email_sent = send_game_links_email(
                            to_email=order.get('customerEmail'),
                            customer_name=order.get('customerName'),
                            order_id=order_id,
                            games=game_details,
                            expires_hours=24
                        )
                        notification_status['games_sent'] = email_sent
                        logger.info(f"TEST WEBHOOK - Game notifications sent: {email_sent}")
                except Exception as e:
                    logger.error(f"TEST WEBHOOK - Failed to send game notifications: {str(e)}")
            
            return {
                'success': True,
                'message': 'Test webhook processed successfully',
                'order_id': order_id,
                'payment_status': payment_status,
                'notifications': notification_status,
                'items_found': {
                    'ebooks': len(ebooks),
                    'games': len(games)
                }
            }
        
        return {
            'success': True,
            'message': 'Order updated but order data not found for notifications',
            'order_id': order_id
        }
        
    except Exception as e:
        logger.error(f"TEST WEBHOOK - Error: {str(e)}", exc_info=True)
        return {
            'success': False,
            'message': f'Error processing test webhook: {str(e)}'
        }


@router.post("/midtrans")
async def midtrans_webhook(request: Request):
    """
    Handle Midtrans payment notification webhook
    """
    from server import db
    
    try:
        # Get webhook data
        data = await request.json()
        logger.info(f"Received webhook data: {data}")
        
        order_id = data.get('order_id')
        transaction_status = data.get('transaction_status')
        fraud_status = data.get('fraud_status')
        status_code = data.get('status_code')
        gross_amount = data.get('gross_amount')
        signature_key = data.get('signature_key')
        transaction_id = data.get('transaction_id')
        payment_type = data.get('payment_type')
        transaction_time = data.get('transaction_time')
        
        # Verify signature
        is_valid = midtrans_service.verify_signature(
            order_id=order_id,
            status_code=status_code,
            gross_amount=gross_amount,
            signature_key=signature_key
        )
        
        if not is_valid:
            logger.error(f"Invalid signature for order {order_id}")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Determine payment status
        payment_status = PaymentStatus.PENDING.value
        notion_link = None
        paid_at = None
        now_utc = datetime.now(timezone.utc)
        
        if transaction_status == 'capture':
            if fraud_status == 'accept':
                payment_status = PaymentStatus.SUCCESS.value
                notion_link = os.environ.get('NOTION_DOWNLOAD_LINK', 'https://notion.so/pelangi-pintar-downloads')
                paid_at = now_utc.isoformat()
        elif transaction_status == 'settlement':
            payment_status = PaymentStatus.SUCCESS.value
            notion_link = os.environ.get('NOTION_DOWNLOAD_LINK', 'https://notion.so/pelangi-pintar-downloads')
            paid_at = now_utc.isoformat()
        elif transaction_status in ['cancel', 'deny', 'expire']:
            payment_status = PaymentStatus.FAILED.value
        elif transaction_status == 'pending':
            payment_status = PaymentStatus.PENDING.value
        
        # Update order
        update_result = await db.orders.update_one(
            {"orderId": order_id},
            {
                "$set": {
                    "paymentStatus": payment_status,
                    "notionDownloadLink": notion_link,
                    "midtransTransactionId": transaction_id,
                    "paidAt": paid_at,
                    "updatedAt": now_utc.isoformat()
                }
            }
        )
        
        if update_result.modified_count == 0:
            logger.warning(f"Order {order_id} not found or not updated")
        
        # Store payment record - handle transaction_time parsing safely
        try:
            if transaction_time:
                # Try to parse transaction_time
                parsed_time = datetime.fromisoformat(transaction_time.replace(' ', 'T'))
                if parsed_time.tzinfo is None:
                    parsed_time = parsed_time.replace(tzinfo=timezone.utc)
                transaction_time_iso = parsed_time.isoformat()
            else:
                transaction_time_iso = now_utc.isoformat()
        except Exception as parse_error:
            logger.warning(f"Failed to parse transaction_time '{transaction_time}': {parse_error}")
            transaction_time_iso = now_utc.isoformat()
        
        payment_record = {
            "orderId": order_id,
            "midtransTransactionId": transaction_id,
            "transactionStatus": transaction_status,
            "paymentType": payment_type,
            "grossAmount": int(float(gross_amount)) if gross_amount else 0,
            "transactionTime": transaction_time_iso,
            "fraudStatus": fraud_status,
            "webhookData": data,
            "createdAt": now_utc.isoformat()
        }
        
        await db.payments.insert_one(payment_record)
        
        logger.info(f"Webhook processed for order {order_id}: {transaction_status}")
        
        # Send notifications if payment is successful
        if payment_status == PaymentStatus.SUCCESS.value:
            try:
                # Get order details
                order = await db.orders.find_one({"orderId": order_id})
                if not order:
                    logger.warning(f"Order {order_id} not found for sending notifications")
                else:
                    logger.info(f"Processing notifications for order {order_id}")
                    # Prepare ebook list with download links
                    ebooks = []
                    games = []
                    
                    for item in order.get('items', []):
                        product_type = item.get('productType', 'ebook')
                        logger.info(f"Processing item: {item.get('title')} (type: {product_type})")
                        
                        if product_type == 'minigame':
                            # Collect game IDs for access token
                            games.append({
                                'id': item.get('ebookId'),
                                'title': item.get('title'),
                                'quantity': item.get('quantity', 1)
                            })
                        elif item.get('driveDownloadLink'):
                            # Regular ebooks
                            ebooks.append({
                                'title': item['title'],
                                'downloadLink': item['driveDownloadLink'],
                                'thumbnail': item.get('thumbnailUrl', ''),
                                'description': item.get('description', ''),
                                'quantity': item.get('quantity', 1)
                            })
                    
                    logger.info(f"Found {len(ebooks)} ebooks and {len(games)} games to notify")
                    
                    # Send ebook notifications if any ebooks purchased
                    if ebooks:
                        try:
                            notification_results = send_order_notifications(
                                customer_email=order.get('customerEmail'),
                                customer_name=order.get('customerName'),
                                customer_phone=order.get('customerPhone', ''),
                                order_id=order_id,
                                ebooks=ebooks
                            )
                            logger.info(f"Ebook notifications sent for order {order_id}: {notification_results}")
                        except Exception as ebook_error:
                            logger.error(f"Failed to send ebook notifications: {str(ebook_error)}", exc_info=True)
                    
                    # Send game links if any games purchased
                    if games:
                        try:
                            from services.notification_service import send_game_links_email
                            
                            # Create 24-hour access tokens for each game
                            game_details = []
                            for game in games:
                                try:
                                    game_data = await db.minigames.find_one({"id": game['id']})
                                    if not game_data:
                                        logger.warning(f"Game {game['id']} not found in database")
                                        continue
                                    
                                    # Create unique access token for this game purchase
                                    token_id = str(uuid.uuid4())
                                    now = datetime.now(timezone.utc)
                                    expires_at = now + timedelta(hours=24)
                                    
                                    # Store access token in database
                                    access_token_doc = {
                                        "tokenId": token_id,
                                        "orderId": order_id,
                                        "gameId": game['id'],
                                        "customerEmail": order.get('customerEmail'),
                                        "customerName": order.get('customerName'),
                                        "gameUrl": game_data.get('gameUrl'),
                                        "createdAt": now.isoformat(),
                                        "expiresAt": expires_at.isoformat(),
                                        "isActive": True,
                                        "accessCount": 0
                                    }
                                    
                                    await db.game_access_tokens.insert_one(access_token_doc)
                                    
                                    # Create proxy URL with token
                                    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
                                    proxy_url = f"{frontend_url}/api/game-access/{token_id}"
                                    
                                    game_details.append({
                                        'id': game['id'],
                                        'title': game_data.get('title'),
                                        'gameUrl': proxy_url,  # Use proxy URL instead of direct URL
                                        'icon': game_data.get('icon', '🎮'),
                                        'thumbnail': game_data.get('thumbnailUrl', ''),
                                        'description': game_data.get('description', ''),
                                        'quantity': game.get('quantity', 1)
                                    })
                                except Exception as game_token_error:
                                    logger.error(f"Failed to create token for game {game['id']}: {str(game_token_error)}", exc_info=True)
                            
                            # Send email with proxy game links (24-hour valid)
                            if game_details:
                                email_sent = send_game_links_email(
                                    to_email=order.get('customerEmail'),
                                    customer_name=order.get('customerName'),
                                    order_id=order_id,
                                    games=game_details,
                                    expires_hours=24
                                )
                                logger.info(f"Game links email sent for order {order_id}: {email_sent}")
                        except Exception as game_error:
                            logger.error(f"Failed to send game notifications: {str(game_error)}", exc_info=True)
                    
            except Exception as notif_error:
                logger.error(f"Error sending notifications for order {order_id}: {str(notif_error)}", exc_info=True)
                # Don't fail the webhook if notification fails
        
        return {
            'success': True,
            'message': 'Webhook processed successfully'
        }
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process webhook: {str(e)}")
