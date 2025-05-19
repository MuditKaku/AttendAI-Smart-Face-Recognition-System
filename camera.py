import cv2
import time
from PIL import Image
import streamlit as st
from face_recognition import verify_face
from attendance import mark_attendance

def run_camera():
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    cam_col, info_col = st.columns([2, 1])

    frame_container = cam_col.empty()
    status_container = cam_col.empty()
    result_container = cam_col.empty()
    info_container = info_col.empty()

    status_container.success("✅ Camera ON - Scanning...")

    last_checked = time.time()
    last_name = "Scanning..."
    info = {}

    while st.session_state.camera_on:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Failed to access camera.")
            break

        frame = cv2.resize(frame, (320, 240))

        if time.time() - last_checked >= 1:
            name, info = verify_face(frame)
            last_checked = time.time()

            if name != "Unknown":
                mark_result = mark_attendance(name)
                result_container.success(mark_result)
            else:
                result_container.warning("⚠️ Unknown face")

            last_name = name

        frame_display = frame.copy()
        cv2.putText(frame_display, last_name, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        frame_container.image(image, channels="RGB", width=320)

        if last_name != "Unknown" and info:
            info_html = f"<b>Name</b>: {last_name}<br>" + "<br>".join(
                [f"<b>{k}</b>: {v}" for k, v in info.items()]
            )
            info_container.markdown(f"<h4>🧾 Student Info</h4>{info_html}", unsafe_allow_html=True)
        else:
            info_container.empty()

        time.sleep(0.02)

    cap.release()
