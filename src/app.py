import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
import asyncio
from inference import TableExtractionPipeline
class TETRStructureRecognition:
    def __init__(self) -> None:
        self.pipe = TableExtractionPipeline(
            det_config_path="detection_config.json",
            det_model_path="models/pubtables1m_detection_detr_r18.pth",
            det_device="cuda",
            str_config_path="structure_config.json",
            str_model_path="models/pubtables1m_structure_detr_r18.pth",
            str_device="cuda",
        )
        self.save_folder = './output'
        self.img_path = 'table_image/1.png'
        self.tokens = []

    async def predict_table(self, img):
        extracted_tables = self.pipe.recognize(
            img, self.tokens, out_objects=True, out_cells=True, out_html=True, out_csv=True
        )
        st.write(extracted_tables["html"][0], unsafe_allow_html=True)
    
if __name__ == "__main__":
    st.header("DETR Table Structure Recognition")
    file = st.file_uploader('Table Image', accept_multiple_files=False, type=['png','jpg'], )
    pts = TETRStructureRecognition()
    if file is not None:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        asyncio.run(pts.predict_table(image))
