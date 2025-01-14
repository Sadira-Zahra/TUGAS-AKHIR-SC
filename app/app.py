import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pandas as pd

# Load the YOLO model
MODEL_PATH = r'C:\Users\LENOVO\Downloads\TUGAS AKHIR SC\app\best1.pt'
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    st.error(f"Failed to load YOLO model: {e}")
    st.stop()

# Title of the app
st.title("Car Damage Detection")

# Mapping class indices to categories, costs, and depth multiplier
class_names = {0: 'Dent', 1: 'Glassbreak', 2: 'Scratch'}
cost_per_area = {0: 8, 1: 3, 2: 2}  # Cost per pixel squared
depth_factor = 5  # Scale factor for depth (specific to Dent)

def calculate_cost(area, cls, confidence):
    """Calculate the cost based on area, class, and confidence."""
    base_cost = area * cost_per_area.get(cls, 0)
    if cls == 0:  # Dent: Apply depth multiplier
        depth = confidence * depth_factor
        return base_cost * depth, depth
    return base_cost, 1.0

# Upload an image
uploaded_file = st.file_uploader("Upload an image to detect damage", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Read and display the uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image', use_column_width=True)
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Perform detection
        results = model(img_bgr)

        detected_items = []
        img_bgr_copy = img_bgr.copy()
        total_cost = 0

        # Process results
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    category = class_names.get(cls, "Unknown")

                    # Calculate area of damage
                    width = x2 - x1
                    height = y2 - y1
                    area = width * height

                    # Calculate cost and depth multiplier
                    cost, depth = calculate_cost(area, cls, conf)

                    # Add detected item
                    detected_items.append({
                        "Item": category,
                        "Width (px)": width,
                        "Height (px)": height,
                        "Area (px^2)": area,
                        "Depth Multiplier": f"{depth:.2f}" if cls == 0 else "-",
                        "Cost per px^2": f"Rp. {cost_per_area.get(cls, 0):.2f}",
                        "Amount": f"Rp. {cost:.2f}"
                    })

                    # Draw bounding box and label
                    cv2.rectangle(img_bgr_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f'{category}: {conf:.2f} ({width}x{height})'
                    if cls == 0:
                        label += f' Depth: {depth:.2f}'
                    cv2.putText(img_bgr_copy, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    total_cost += cost

        # Convert BGR to RGB for displaying
        img_rgb_detected = cv2.cvtColor(img_bgr_copy, cv2.COLOR_BGR2RGB)

        # Display images
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption='Uploaded Image', use_column_width=True)
        with col2:
            st.image(img_rgb_detected, caption='Detected Image', use_column_width=True)

        # Calculate summary
        subtotal = total_cost
        tax = subtotal * 0.10
        total = subtotal + tax

        # Create DataFrame
        if detected_items:
            df = pd.DataFrame(detected_items)
        else:
            df = pd.DataFrame(columns=["Item", "Width (px)", "Height (px)", "Area (px^2)", "Depth Multiplier", "Cost per px^2", "Amount"])

        summary_rows = [
            {"Item": "Subtotal", "Width (px)": "", "Height (px)": "", "Area (px^2)": "", "Depth Multiplier": "", "Cost per px^2": "", "Amount": f"Rp. {subtotal:.2f}"},
            {"Item": "Tax (10%)", "Width (px)": "", "Height (px)": "", "Area (px^2)": "", "Depth Multiplier": "", "Cost per px^2": "", "Amount": f"Rp. {tax:.2f}"},
            {"Item": "Total", "Width (px)": "", "Height (px)": "", "Area (px^2)": "", "Depth Multiplier": "", "Cost per px^2": "", "Amount": f"Rp. {total:.2f}"}
        ]
        df = pd.concat([df, pd.DataFrame(summary_rows)], ignore_index=True)

        # Display table
        st.write("### Order Summary")
        st.table(df)

    except Exception as e:
        st.error(f"Error processing image: {e}")
