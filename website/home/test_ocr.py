from home.ocr_utils import extract_text_from_image # type: ignore

image_path = 'printed.png'  # Use the relative path
text = extract_text_from_image(image_path)
print("Extracted Text:\n")
print(text)