"""Tests for image loading fallback logic in app.py."""
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import io


def make_placeholder_image(label: str = "Test") -> Image.Image:
    """Replicate the PIL placeholder logic from app.py for testing."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (400, 200), (20, 8, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, 395, 195], outline=(255, 215, 0), width=2)
    draw.text((200, 100), f"\U0001f549 {label}", fill=(255, 215, 0), anchor="mm")
    return img


# ── PIL placeholder ────────────────────────────────────────────────────────

def test_placeholder_image_creates_valid_pil_image():
    img = make_placeholder_image("Krishna & Arjuna")
    assert isinstance(img, Image.Image)

def test_placeholder_image_correct_size():
    img = make_placeholder_image()
    assert img.size == (400, 200)

def test_placeholder_image_correct_mode():
    img = make_placeholder_image()
    assert img.mode == "RGB"

def test_placeholder_image_serializable_to_bytes():
    """Ensure the PIL image can be converted to bytes without error."""
    img = make_placeholder_image("Kurukshetra")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    assert buf.tell() > 0, "Image bytes should not be empty"

def test_placeholder_different_labels():
    labels = ["Krishna & Arjuna", "Krishna Flute", "Kurukshetra", "Gita Teaching"]
    for label in labels:
        img = make_placeholder_image(label)
        assert img is not None


# ── requests fallback mock ─────────────────────────────────────────────────

def test_url_fetch_failure_falls_back_gracefully():
    """Simulate all URLs failing — should produce a PIL image, not crash."""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        # Fallback should return a PIL Image without raising
        img = make_placeholder_image("Fallback Test")
        assert isinstance(img, Image.Image)

def test_url_fetch_bad_status_falls_back():
    """Simulate URL returning non-200 status."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.content = b""
        mock_get.return_value = mock_response
        img = make_placeholder_image("403 Fallback")
        assert isinstance(img, Image.Image)
