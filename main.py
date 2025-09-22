import cv2
import mediapipe as mp
import time
from gesture_detector import GestureDetector
from macro_executor import MacroExecutor
from video_capturer import VideoCapturer

def main():
    video_capturer = VideoCapturer()
    gesture_detector = GestureDetector()
    macro_executor = MacroExecutor()
    last_gesture = None
    pause_delay = 0.5   # 500ms delay when paused or no hand
    print("Starting gesture macro app. Press 'q' to quit.")
    while True:
        ret, frame = video_capturer.get_frame()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame for natural interaction
        frame = cv2.flip(frame, 1)

        # Detect gesture using MediaPipe
        gesture = gesture_detector.detect(frame)
        if gesture == 'Paused':
            print("Gesture detection paused. Show 'rock' again to resume.")
        elif gesture == 'Resumed':
            print("Gesture detection resumed.")

        if gesture != last_gesture and gesture is not None:
            if gesture_detector.paused:
                macro_executor.execute(gesture)
            last_gesture = gesture
        elif gesture is None:
            last_gesture = None

        cv2.imshow('GestureMacroApp', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if gesture_detector.paused or gesture is None:
            time.sleep(pause_delay)

    video_capturer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
