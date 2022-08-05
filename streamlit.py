import pickle
import streamlit as st
import cv2
from PIL import Image
import requests

from skimage.metrics import structural_similarity
import os
import pathlib


loaded_model = pickle.load(
    open("trained_model.sav", "rb"))


def tampering_detector(input_image):
    pathName = "images/original.png"

    original_image = cv2.imread(pathName)
    tamp_image = Image.open(input_image).resize((224, 224))

    tamp_image.save(
        "images/tamp.png")
    st.image(tamp_image)
    tampered_image = cv2.imread(
        "   images/tamp.png")

    original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    tampered_gray = cv2.cvtColor(tampered_image, cv2.COLOR_BGR2GRAY)

    (loaded_model, diff) = structural_similarity(
        original_gray, tampered_gray, full=True)
    diff = (diff*255).astype("uint8")
    return loaded_model


def main():
    st.title("PAN CARD TAMPERING DETECTOR")

    detection = ""

    image = st.file_uploader("Upload Images", type=["png", "jpeg", "jpg"])

    if st.button("Detect Tampering"):
        detection = tampering_detector(image)
        if detection < 0.5:
            st.error(f"Fake at {round(detection*100)} % ")
        else:
            st.success("Original")


if __name__ == '__main__':
    main()
