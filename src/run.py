from inference import TableExtractionPipeline
from PIL import Image, ImageDraw

# Create inference pipeline
pipe = TableExtractionPipeline(
    det_config_path="detection_config.json",
    det_model_path="models/pubtables1m_detection_detr_r18.pth",
    det_device="cuda",
    str_config_path="structure_config.json",
    str_model_path="models/pubtables1m_structure_detr_r18.pth",
    str_device="cuda",
)

img = Image.open("image/anthem-2017-def_14a-t101.png")
tokens = [
    {"bbox": [0.0, 0.0, 50.0, 50.0], "text": "First"},
    {"bbox": [52.0, 0.0, 102.0, 50.0], "text": "next"},
]
# Recognize table(s) from image
extracted_tables = pipe.recognize(
    img, tokens, out_objects=True, out_cells=True, out_html=True, out_csv=True
)

# Select table (there could be more than one)
extracted_table = extracted_tables

# Get output in desired format
objects = extracted_table["objects"]
cells = extracted_table["cells"]
csv = extracted_table["csv"]
html = extracted_table["html"]

for cell in cells[0]:
    shape = [(cell["bbox"][0], cell["bbox"][1]), (cell["bbox"][2], cell["bbox"][3])]
    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle(shape, outline="green")
img.show()
print(html)