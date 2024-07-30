import streamlit as st
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

st.title("Hand Gesture Drag-and-Drop")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200 

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList, _ = detector.findPosition(frame)
    
    global cx, cy, colorR
    
    if lmList:
        l, _, _ = detector.findDistance(8, 12, frame)
        if l < 30:
            cursor = lmList[8]
            if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                colorR = (0, 255, 0)
                cx, cy = cursor[0], cursor[1]
            else:
                colorR = (255, 0, 255)
    
    cv2.rectangle(frame, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    return frame

def main():
    stframe = st.empty()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.write("Failed to capture image")
            break
        
        frame = process_frame(frame)
        stframe.image(frame, channels="BGR")

if __name__ == "__main__":
    main()
