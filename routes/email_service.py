# routes/email_service.py
import os, smtplib, ssl, asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER or "no-reply@example.com")

def _render_html(order: dict, products: List[dict]) -> str:
    lines = []
    lines.append(f"<p>Terima kasih! Order <b>#{order.get('orderId')}</b> telah <b>berhasil dibayar</b>.</p>")
    if products:
        lines.append("<ul>")
        for p in products:
            title = p.get("title") or "Produk"
            ptype = p.get("product_type") or "ebook"
            file_url = p.get("file_url")
            external_url = p.get("external_url")
            # Tampilkan tautan yang relevan
            if ptype in ("ebook", "ebook_exclusive") and file_url:
                lines.append(f'<li>{title} — <a href="{file_url}" target="_blank" rel="noopener">Download</a></li>')
            elif ptype == "minigame" and external_url:
                lines.append(f'<li>{title} — <a href="{external_url}" target="_blank" rel="noopener">Mainkan</a></li>')
            else:
                lines.append(f"<li>{title}</li>")
        lines.append("</ul>")
    lines.append("<p>Jika tautan tidak berfungsi, balas email ini ya.</p>")
    return "\n".join(lines)

async def send_order_email(to_email: str, order: dict, products: List[dict]) -> None:
    """
    Kirim email sederhana via SMTP (TLS). ENV wajib:
    SMTP_HOST, SMTP_PORT(=587), SMTP_USER, SMTP_PASS, MAIL_FROM
    """
    if not to_email or not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        # Jangan gagalkan webhook kalau SMTP belum dikonfigurasi.
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"EbookAnak — Order #{order.get('orderId')} Paid"
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
