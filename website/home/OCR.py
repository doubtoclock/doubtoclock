import os
import cv2
import torch
import numpy as np
from PIL import Image
import easyocr
from spellchecker import SpellChecker
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize models
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-printed")
trocr = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-printed").to(device)
spell = SpellChecker()


def preprocess_crop_otsu(crop):
    cv_img = np.array(crop)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary_img).convert("RGB")


def trocr_recognize_pil(image_pil):
    inputs = processor(images=image_pil, return_tensors="pt")
    pixel_values = inputs.pixel_values.to(device)
    with torch.no_grad():
        generated_ids = trocr.generate(pixel_values, max_length=128, num_beams=32, early_stopping=True)
    pred_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return pred_text.strip()


def extract_text_line_by_line(image_pil, y_tol=20, pad=8, min_size=40):
    np_img = np.array(image_pil)[:, :, ::-1]
    detections = reader.readtext(np_img)
    if not detections:
        return []

    results = []
    for _, text, conf in detections:
        try:
            corrected = " ".join([spell.correction(w) for w in text.split()])
        except Exception:
            corrected = text
        results.append((text, corrected, conf))

    return results


def extract_text_from_image(image_path):
    """Main function to call from your Django view"""
    image = Image.open(image_path).convert("RGB")
    lines = extract_text_line_by_line(image)
    final_text = "\n".join([line[1] for line in lines])
    return final_text
