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
    frame_delay = 0.05  # 50ms delay ~ 20 FPS

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
        if gesture != last_gesture and gesture is not None:
            macro_executor.execute(gesture)
            last_gesture = gesture
        elif gesture is None:
            last_gesture = None

        cv2.imshow('GestureMacroApp', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(frame_delay)

    video_capturer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
