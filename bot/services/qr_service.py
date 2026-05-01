"""
bot/services/qr_service.py — Generate QR code images in-memory.
"""
from __future__ import annotations

import io

import qrcode
from qrcode.image.pil import PilImage


def generate_qr_bytes(data: str) -> bytes:
    """Return a PNG QR code as raw bytes (no disk I/O)."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
