# ai_models_app/adapters/cxr.py
from __future__ import annotations
import io
from typing import Dict, List, Tuple
from PIL import Image, ImageOps
import numpy as np
from django.conf import settings

try:
    import torch
    TORCH = True
except Exception:
    TORCH = False

DEFAULT_LABELS = [
    "Atelectasis","Cardiomegaly","Consolidation","Edema","Pleural Effusion",
    "Enlarged Cardiomediastinum","Lung Lesion","Lung Opacity","Pneumonia",
    "Pneumothorax","Fracture","Pleural Other","Support Devices","No Finding"
]

def _load_torch_model():
    if not TORCH:
        return None
    w = getattr(settings, "CXR_WEIGHTS_PATH", None)
    if not w:
        return None
    m = torch.jit.load(str(w), map_location="cuda" if torch.cuda.is_available() else "cpu")
    m.eval()
    return m

_MODEL = None

def _ensure_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = _load_torch_model()
    return _MODEL

def _preprocess(img: Image.Image, size: int = 320):
    img = ImageOps.exif_transpose(img).convert("RGB").resize((size, size))
    arr = np.asarray(img).astype("float32") / 255.0
    arr = (arr - 0.5) / 0.25
    arr = np.transpose(arr, (2, 0, 1))
    return torch.from_numpy(arr).unsqueeze(0)

def predict_probs(img: Image.Image, labels: List[str] | None = None) -> Dict[str, float]:
    labels = labels or getattr(settings, "CXR_LABELS", DEFAULT_LABELS)
    model = _ensure_model()
    if TORCH and model is not None:
        with torch.no_grad():
            x = _preprocess(img).to(next(model.parameters()).device)
            logits = model(x)
            if isinstance(logits, (list, tuple)): logits = logits[0]
            probs = torch.sigmoid(logits).squeeze(0).detach().cpu().numpy().tolist()
        L = min(len(probs), len(labels))
        return {labels[i]: float(probs[i]) for i in range(L)}
    # fallback: خروجی ساختگی
    return {lbl: 0.2 for lbl in labels}

def top_findings(probs: Dict[str, float], k: int = 5, th: float = 0.3) -> List[Tuple[str, float]]:
    items = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    return [(n, float(p)) for n, p in items[:k] if p >= th]

def make_overlay(img: Image.Image) -> Image.Image:
    """Placeholder overlay: قاب قرمز باریک دور تصویر"""
    base = img.convert("RGBA")
    w, h = base.size
    for x in range(w):
        if x < 3 or x >= w-3:
            for y in range(h): base.putpixel((x, y), (255, 0, 0, 255))
    for y in range(h):
        if y < 3 or y >= h-3:
            for x in range(w): base.putpixel((x, y), (255, 0, 0, 255))
    return base

def narrative(findings: List[Tuple[str, float]]) -> str:
    if not findings:
        return "یافته شاخصی گزارش نشد. تفسیر بالینی و مقایسه با تصاویر قبلی پیشنهاد می‌شود."
    lines = [f"{i+1}. {name}: احتمال {int(p*100)}٪" for i, (name, p) in enumerate(findings)]
    return "خلاصه:\n" + "\n".join(lines) + "\n\nاین نتیجه صرفاً آموزشی است و جایگزین تشخیص/درمان نیست."
