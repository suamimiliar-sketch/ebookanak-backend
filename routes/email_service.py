# routes/email_service.py
import os, smtplib, ssl, asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER or "no-reply@example.com")

def _render_html(order: dict, products: list[dict]) -> str:
    # Email sederhana dengan link produk
    lines = []
    lines.append(f"<p>Terima kasih! Order <b>#{order.get('id')}</b> telah <b>paid</b>.</p>")
    if products:
        lines.append("<ul>")
        for p in products:
            title = p.get("title") or "Produk"
            if p.get("product_type") == "ebook" and p.get("file_url"):
                lines.append(f'<li>{title} — <a href="{p["file_url"]}" target="_blank" rel="noopener">Download</a></li>')
            elif p.get("product_type") == "minigame" and p.get("external_url"):
                lines.append(f'<li>{title} — <a href="{p["external_url"]}" target="_blank" rel="noopener">Mainkan</a></li>')
            else:
                lines.append(f'<li>{title}</li>')
        lines.append("</ul>")
    lines.append('<p>Jika link tidak berfungsi, balas email ini ya.</p>')
    return "\n".join(lines)

async def send_order_email(to_email: str, order: dict, products: list[dict]) -> None:
    if not to_email or not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        # Jika SMTP belum diset, jangan error-kan webhook—cukup diam.
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"EbookAnak — Order #{order.get('id')} Paid"
    msg["From"] = MAIL_FROM
    msg["To"] = to_email

    html = _render_html(order, products)
    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()

    def _send():
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(MAIL_FROM, [to_email], msg.as_string())

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send)
