"""
Notification service for sending emails and WhatsApp messages
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from twilio.rest import Client


# Email configuration
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')


def create_email_html(customer_name: str, order_id: str, ebooks: List[Dict]) -> str:
    """Create simplified HTML email template for download links - spam filter friendly"""
    
    # Simplified list of ebooks - no images to reduce spam score
    ebook_links_html = ""
    for i, ebook in enumerate(ebooks, 1):
        ebook_links_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">
                <strong>{i}. {ebook['title']}</strong><br>
                <a href="{ebook['downloadLink']}" style="color: #4CAF50; text-decoration: none; font-weight: 600;">
                    Download Ebook
                </a>
            </td>
        </tr>
        """
    
    # Plain text version for better deliverability
    plain_text = f"""
Pelangi Pintar - Platform Edukasi Anak Indonesia

Halo {customer_name},

Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.

Order ID: {order_id}

📚 DOWNLOAD EBOOK ANDA:
"""
    
    for i, ebook in enumerate(ebooks, 1):
        plain_text += f"\n{i}. {ebook['title']}\n   {ebook['downloadLink']}\n"
    
    plain_text += """
💡 CATATAN PENTING:
Link download bersifat permanen. Simpan email ini untuk akses kapan saja.

Butuh bantuan?
📧 pelangipintar@ebookanak.store
📱 +62 823 6545 9989

© 2025 Pelangi Pintar. All rights reserved.
"""
    
    # Simplified HTML version - minimal styling to avoid spam filters
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; padding: 20px; background: #667eea; color: white; border-radius: 8px;">
        <h1 style="margin: 0; font-size: 24px;">Pelangi Pintar</h1>
        <p style="margin: 5px 0 0 0;">Platform Edukasi Anak Indonesia</p>
    </div>
    
    <div style="padding: 20px; background: #f9f9f9; margin: 20px 0; border-radius: 8px;">
        <h2 style="margin: 0 0 10px 0; font-size: 18px;">Halo, {customer_name}!</h2>
        <p style="margin: 0 0 10px 0;">Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.</p>
        <p style="margin: 0; color: #666;"><strong>Order ID:</strong> {order_id}</p>
    </div>
    
    <h3 style="margin: 20px 0 10px 0;">📚 Ebook Anda</h3>
    <table style="width: 100%; border-collapse: collapse;">
        {ebook_links_html}
    </table>
    
    <div style="padding: 15px; background: #fffbea; border-left: 4px solid #ffc107; margin: 20px 0; border-radius: 4px;">
        <p style="margin: 0 0 5px 0; font-weight: bold;">💡 Catatan Penting</p>
        <p style="margin: 0;">Link download bersifat permanen. Simpan email ini untuk akses kapan saja.</p>
    </div>
    
    <div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; margin-top: 20px;">
        <p style="margin: 0 0 10px 0; font-weight: bold;">Butuh bantuan?</p>
        <p style="margin: 0;">📧 pelangipintar@ebookanak.store</p>
        <p style="margin: 5px 0 10px 0;">📱 +62 823 6545 9989</p>
        <p style="margin: 0; color: #999; font-size: 12px;">© 2025 Pelangi Pintar</p>
    </div>
</body>
</html>"""
    
    return html, plain_text


def send_email(to_email: str, customer_name: str, order_id: str, ebooks: List[Dict]) -> bool:
    """Send email with download links - multipart (plain text + HTML)"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Download Ebook Anda - Order #{order_id}'  # Removed emoji to avoid spam
        msg['From'] = f"Pelangi Pintar <{SMTP_EMAIL}>"
        msg['To'] = to_email
        msg['Reply-To'] = SMTP_EMAIL
        
        # Create both plain text and HTML content
        html_content, plain_text_content = create_email_html(customer_name, order_id, ebooks)
        
        # Attach plain text first (fallback)
        text_part = MIMEText(plain_text_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # Attach HTML second (preferred)
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Send email using SSL
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False



def create_game_access_email_html(customer_name: str, order_id: str, access_token: str, games: List[Dict], expires_in_hours: int = 24) -> str:
    """Create HTML email template for game access link"""
    
    access_link = f"{FRONTEND_URL}/games/play?token={access_token}"
    
    games_html = ""
    for game in games:
        games_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">
                <span style="font-size: 24px;">🎮</span>
                <span style="margin-left: 10px; color: #333; font-size: 16px;">Mini Game #{game['id']}</span>
            </td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 40px 0; text-align: center; background: linear-gradient(135deg, #FFB6C1 0%, #E6E6FA 100%);">
                    <h1 style="margin: 0; color: white; font-size: 32px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                        🌈 Pelangi Pintar
                    </h1>
                    <p style="margin: 10px 0 0 0; color: white; font-size: 16px;">
                        Platform Edukasi Anak
                    </p>
                </td>
            </tr>
            <tr>
                <td style="padding: 0;">
                    <table role="presentation" style="width: 600px; margin: 40px auto; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; max-width: 100%;">
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #333; font-size: 24px;">
                                    🎉 Halo, {customer_name}!
                                </h2>
                                <p style="margin: 0 0 20px 0; color: #666; font-size: 16px; line-height: 1.6;">
                                    Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.
                                </p>
                                
                                <div style="background-color: #FFF8E7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                                    <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">
                                        <strong>Order ID:</strong> {order_id}
                                    </p>
                                    <p style="margin: 0; color: #666; font-size: 14px;">
                                        <strong>Akses Berlaku:</strong> {expires_in_hours} Jam
                                    </p>
                                </div>
                                
                                <h3 style="margin: 30px 0 15px 0; color: #333; font-size: 20px;">
                                    🎮 Game yang Tersedia:
                                </h3>
                                
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 30px 0;">
                                    {games_html}
                                </table>
                                
                                <div style="text-align: center; margin: 30px 0;">
                                    <a href="{access_link}" 
                                       style="display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #FF8B94 0%, #FFB88C 100%); 
                                              color: white; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 18px;
                                              box-shadow: 0 4px 15px rgba(255, 139, 148, 0.3);">
                                        🚀 Mainkan Sekarang!
                                    </a>
                                </div>
                                
                                <div style="background-color: #F0FFFA; padding: 20px; border-radius: 8px; border-left: 4px solid #7FD8BE;">
                                    <p style="margin: 0 0 10px 0; color: #333; font-size: 14px; font-weight: bold;">
                                        💡 Catatan Penting:
                                    </p>
                                    <ul style="margin: 0; padding-left: 20px; color: #666; font-size: 14px; line-height: 1.8;">
                                        <li>Link akses berlaku selama {expires_in_hours} jam dari waktu pembelian</li>
                                        <li>Simpan link ini untuk mengakses game kapan saja</li>
                                        <li>Game dapat dimainkan berulang kali dalam periode akses</li>
                                    </ul>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 30px; background-color: #FFF5F7; text-align: center; border-top: 1px solid #FFB6C1;">
                                <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">
                                    Ada pertanyaan? Hubungi kami:
                                </p>
                                <p style="margin: 0; color: #FF8B94; font-size: 14px;">
                                    📧 pelangipintar@ebookanak.store
                                </p>
                                <p style="margin: 10px 0 0 0; color: #666; font-size: 12px;">
                                    © 2024 Pelangi Pintar. Semua hak dilindungi.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def send_game_links_email(to_email: str, customer_name: str, order_id: str, games: List[Dict], expires_hours: int = 24) -> bool:
    """Send email with direct game links - simplified for better deliverability"""
    try:
        # Check if SMTP is configured
        if not SMTP_HOST or not SMTP_EMAIL or not SMTP_PASSWORD:
            print("⚠️ SMTP not configured, skipping game links email")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Link Game Anda - Order #{order_id}'  # Removed emoji
        msg['From'] = f"Pelangi Pintar <{SMTP_EMAIL}>"
        msg['To'] = to_email
        msg['Reply-To'] = SMTP_EMAIL
        
        # Plain text version
        plain_text = f"""
Pelangi Pintar - Platform Edukasi Anak Indonesia

Halo {customer_name},

Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.

Order ID: {order_id}
Link berlaku: {expires_hours} Jam

MAINKAN GAME ANDA:
"""
        
        # Simplified HTML and plain text lists
        games_html = ""
        for i, game in enumerate(games, 1):
            game_url = game['gameUrl']
            if game_url.startswith('/'):
                game_url = f"{FRONTEND_URL}{game_url}"
            
            # Plain text
            plain_text += f"\n{i}. {game['title']}\n   {game_url}\n"
            
            # HTML
            games_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #ddd;">
                    <strong>{i}. {game['title']}</strong><br>
                    <a href="{game_url}" style="color: #FF8B94; text-decoration: none; font-weight: 600;">
                        Mainkan Game
                    </a>
                </td>
            </tr>
            """
        
        plain_text += f"""
CATATAN PENTING:
- Link berlaku {expires_hours} jam dari waktu pembelian
- Game dapat dimainkan berulang kali dalam periode {expires_hours} jam
- Klik link untuk langsung bermain

Butuh bantuan?
📧 pelangipintar@ebookanak.store
📱 +62 823 6545 9989

© 2025 Pelangi Pintar
"""
        
        # Simplified HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; padding: 20px; background: #667eea; color: white; border-radius: 8px;">
        <h1 style="margin: 0; font-size: 24px;">Pelangi Pintar</h1>
        <p style="margin: 5px 0 0 0;">Platform Edukasi Anak Indonesia</p>
    </div>
    
    <div style="padding: 20px; background: #f9f9f9; margin: 20px 0; border-radius: 8px;">
        <h2 style="margin: 0 0 10px 0; font-size: 18px;">Halo, {customer_name}!</h2>
        <p style="margin: 0 0 10px 0;">Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.</p>
        <p style="margin: 0; color: #666;"><strong>Order ID:</strong> {order_id}</p>
        <p style="margin: 5px 0 0 0; color: #d84315;"><strong>Link berlaku: {expires_hours} Jam</strong></p>
    </div>
    
    <h3 style="margin: 20px 0 10px 0;">Mini Game Anda</h3>
    <table style="width: 100%; border-collapse: collapse;">
        {games_html}
    </table>
    
    <div style="padding: 15px; background: #e8f5e9; border-left: 4px solid #4caf50; margin: 20px 0; border-radius: 4px;">
        <p style="margin: 0 0 5px 0; font-weight: bold;">Catatan Penting</p>
        <ul style="margin: 0; padding-left: 20px;">
            <li>Link berlaku {expires_hours} jam dari waktu pembelian</li>
            <li>Game dapat dimainkan berulang kali</li>
        </ul>
    </div>
    
    <div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; margin-top: 20px;">
        <p style="margin: 0 0 10px 0; font-weight: bold;">Butuh bantuan?</p>
        <p style="margin: 0;">pelangipintar@ebookanak.store</p>
        <p style="margin: 5px 0 10px 0;">+62 823 6545 9989</p>
        <p style="margin: 0; color: #999; font-size: 12px;">© 2025 Pelangi Pintar</p>
    </div>
</body>
</html>"""
        
        # Attach plain text first
        text_part = MIMEText(plain_text, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # Attach HTML second
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Send email using SSL
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Game links email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending game links email: {str(e)}")
        return False


def send_game_access_email(to_email: str, customer_name: str, order_id: str, access_token: str, games: List[Dict], expires_in_hours: int = 24) -> bool:
    """Send email with game access link"""
    try:
        # Check if SMTP is configured
        if not SMTP_HOST or not SMTP_EMAIL or not SMTP_PASSWORD:
            print("⚠️ SMTP not configured, skipping game access email")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🎮 Akses Game Anda - Pelangi Pintar (Order #{order_id})'
        msg['From'] = f"Pelangi Pintar <{SMTP_EMAIL}>"
        msg['To'] = to_email
        
        # Create HTML content
        html_content = create_game_access_email_html(customer_name, order_id, access_token, games, expires_in_hours)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email using SSL
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Game access email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending game access email: {str(e)}")
        return False



def create_whatsapp_message(customer_name: str, order_id: str, ebooks: List[Dict]) -> str:
    """Create WhatsApp message text"""
    message = f"""🦉 *Pelangi Pintar*

Halo {customer_name}! 👋

Terima kasih atas pembelian Anda! Pembayaran telah berhasil diproses.

📋 *Order ID:* {order_id}

📚 *Download Ebook Anda:*
"""
    
    for i, ebook in enumerate(ebooks, 1):
        message += f"\n{i}. *{ebook['title']}*\n"
        message += f"   {ebook['downloadLink']}\n"
    
    message += f"""
💡 *Tips:* Link download ini bersifat permanen. Simpan pesan ini untuk akses di kemudian hari.

📧 Email: pelangipintar@ebookanak.store
📱 WhatsApp: +62 823 6545 9989

Selamat belajar! 🎉
"""
    return message


def send_whatsapp(to_phone: str, customer_name: str, order_id: str, ebooks: List[Dict]) -> bool:
    """Send WhatsApp message with download links"""
    # WhatsApp is currently disabled - will be configured later with Mekari Qontak
    print("ℹ️ WhatsApp notifications are currently disabled")
    return False
    
    try:
        # Check if Twilio is configured
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            print("⚠️ Twilio credentials not configured, skipping WhatsApp notification")
            return False
        
        # Format phone number for WhatsApp
        if not to_phone.startswith('whatsapp:'):
            # Remove any non-digit characters
            phone_digits = ''.join(filter(str.isdigit, to_phone))
            # Add country code if not present (assuming Indonesia +62)
            if not phone_digits.startswith('62'):
                phone_digits = '62' + phone_digits
            to_phone = f'whatsapp:+{phone_digits}'
        
        # Create Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Create message text
        message_text = create_whatsapp_message(customer_name, order_id, ebooks)
        
        # Send message
        message = client.messages.create(
            body=message_text,
            from_=TWILIO_WHATSAPP_FROM,
            to=to_phone
        )
        
        print(f"✅ WhatsApp message sent successfully to {to_phone}, SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {str(e)}")
        return False


def send_order_notifications(
    customer_email: str,
    customer_name: str,
    customer_phone: str,
    order_id: str,
    ebooks: List[Dict]
) -> Dict[str, bool]:
    """Send both email and WhatsApp notifications"""
    
    results = {
        'email_sent': False,
        'whatsapp_sent': False
    }
    
    # Send email
    results['email_sent'] = send_email(customer_email, customer_name, order_id, ebooks)
    
    # Send WhatsApp
    results['whatsapp_sent'] = send_whatsapp(customer_phone, customer_name, order_id, ebooks)
    
    return results
