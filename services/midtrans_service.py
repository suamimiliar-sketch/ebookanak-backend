import midtransclient
import os
import hashlib
from typing import Dict, Any
from datetime import datetime


class MidtransService:
    def __init__(self):
        self.server_key = os.environ.get('MIDTRANS_SERVER_KEY', '')
        self.client_key = os.environ.get('MIDTRANS_CLIENT_KEY', '')
        self.is_production = os.environ.get('MIDTRANS_IS_PRODUCTION', 'false').lower() == 'true'
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Midtrans Init - Server Key: {self.server_key[:15]}... (len: {len(self.server_key)})")
        logger.info(f"Midtrans Init - Client Key: {self.client_key[:15]}... (len: {len(self.client_key)})")
        logger.info(f"Midtrans Init - Is Production: {self.is_production}")
        
        # Initialize Snap API
        self.snap = midtransclient.Snap(
            is_production=self.is_production,
            server_key=self.server_key,
            client_key=self.client_key
        )
    
    def create_transaction(self, order_id: str, customer_name: str, customer_email: str, 
                          items: list, total: int, discount: int = 0, customer_phone: str = '') -> Dict[str, Any]:
        """
        Create Midtrans Snap transaction
        """
        # Format items for Midtrans
        item_details = []
        for item in items:
            item_details.append({
                'id': str(item['ebookId']),
                'price': item['price'],
                'quantity': item['quantity'],
                'name': item['title']
            })
        
        # Add discount as a line item if applicable
        if discount > 0:
            item_details.append({
                'id': 'DISCOUNT',
                'price': -discount,  # Negative price for discount
                'quantity': 1,
                'name': 'Bundle Discount (Every 5 items)'
            })
        
        # Transaction parameters
        param = {
            'transaction_details': {
                'order_id': order_id,
                'gross_amount': total
            },
            'item_details': item_details,
            'customer_details': {
                'first_name': customer_name,
                'email': customer_email,
                'phone': customer_phone if customer_phone else '+62812345678',
                'billing_address': {
                    'first_name': customer_name,
                    'email': customer_email,
                    'phone': customer_phone if customer_phone else '+62812345678',
                    'address': 'Indonesia',
                    'city': 'Jakarta',
                    'postal_code': '12345',
                    'country_code': 'IDN'
                }
            },
            'enabled_payments': [
                'credit_card', 'gopay', 'bank_transfer', 'qris'
            ]
        }
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Creating Midtrans transaction with params: {param}")
            
            transaction = self.snap.create_transaction(param)
            
            logger.info(f"Midtrans response: {transaction}")
            
            return {
                'success': True,
                'token': transaction['token'],
                'redirect_url': transaction['redirect_url']
            }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Midtrans transaction creation failed: {str(e)}")
            logger.error(f"Params sent: {param}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_signature(self, order_id: str, status_code: str, gross_amount: str, 
                        signature_key: str) -> bool:
        """
        Verify Midtrans webhook signature
        """
        string_to_hash = f"{order_id}{status_code}{gross_amount}{self.server_key}"
        calculated_signature = hashlib.sha512(string_to_hash.encode('utf-8')).hexdigest()
        return calculated_signature == signature_key
    
    def get_transaction_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get transaction status from Midtrans
        """
        try:
            core_api = midtransclient.CoreApi(
                is_production=self.is_production,
                server_key=self.server_key,
                client_key=self.client_key
            )
            status = core_api.transactions.status(order_id)
            return {
                'success': True,
                'data': status
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
