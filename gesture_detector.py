import cv2
import mediapipe as mp
import numpy as np
from gesture_patterns import is_peace, is_open_palm, is_fist, is_open_index, is_rock

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.8,
                                         min_tracking_confidence=0.8)
        self.mp_draw = mp.solutions.drawing_utils
        self.paused = False

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        gesture = None
        self.index_history = getattr(self, 'index_history', [])
        self.index_traj = getattr(self, 'index_traj', [])
        self.last_volume_y = getattr(self, 'last_volume_y', None)
        palm_tips_x = []
        # Track all finger tip positions for open palm swipe
        if results.multi_hand_landmarks:
            gesture = ""
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark
                # Pause/resume detection on rock gesture
                if is_rock(lm):
                    self.paused = not self.paused
                    return 'Paused' if self.paused else 'Resumed'
                # Use pattern matching for gestures
                if is_peace(lm):
                    gesture = "Peace"
                # Track all finger tip positions for open palm swipe
                tip_indices = [4, 8, 12, 16, 20]
                palm_tips_x = [lm[i].x for i in tip_indices]
                self.palm_history = getattr(self, 'palm_history', [])
                avg_x = sum(palm_tips_x) / len(palm_tips_x)
                self.palm_history.append(avg_x)
                if len(self.palm_history) > 10:
                    self.palm_history.pop(0)
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Track index finger tip position
                index_tip = lm[8]
                self.index_history.append(index_tip.x)
                self.index_traj.append((index_tip.x, index_tip.y))
                if len(self.index_history) > 10:
                    self.index_history.pop(0)
                if len(self.index_traj) > 20:
                    self.index_traj.pop(0)
                # Detect open palm swipe gestures
                if is_open_palm(lm):
                    self.palm_history = getattr(self, 'palm_history', [])
                    tip_indices = [4, 8, 12, 16, 20]
                    palm_tips_x = [lm[i].x for i in tip_indices]
                    avg_x = sum(palm_tips_x) / len(palm_tips_x)
                    self.palm_history.append(avg_x)
                    if len(self.palm_history) > 10:
                        self.palm_history.pop(0)
                    if len(self.palm_history) >= 10:
                        delta = self.palm_history[-1] - self.palm_history[0]
                        if delta > 0.2:
                            gesture = "Open Palm Right"
                            self.palm_history.clear()
                        elif delta < -0.2:
                            gesture = "Open Palm Left"
                            self.palm_history.clear()
                # Volume control: circle with index finger up only
                if is_open_index(lm):
                    if len(self.index_traj) == 20:
                        gesture_cw = self._detect_circle(self.index_traj, direction='cw')
                        gesture_ccw = self._detect_circle(self.index_traj, direction='ccw')
                        if gesture_cw:
                            gesture = "Circle Clockwise"
                            self.index_traj.clear()
                        elif gesture_ccw:
                            gesture = "Circle Anti-Clockwise"
                            self.index_traj.clear()

        else:
            self.index_history = []
            self.index_traj = []
            self.palm_history = []
            self.last_volume_y = None
        return gesture

    def _recognize_gesture(self, hand_landmarks):
        # Get landmark coordinates
        tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        fingers = []
        lm = hand_landmarks.landmark
        # Thumb
        fingers.append(lm[tips_ids[0]].x < lm[tips_ids[0] - 1].x)
        # Other fingers
        for i in range(1, 5):
            fingers.append(lm[tips_ids[i]].y < lm[tips_ids[i] - 2].y)
        if all(fingers):
            return "Open Palm"
        if not any(fingers):
            return "Fist"
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            return "Peace"
        return None

    def _detect_circle(self, traj, direction='cw'):
        # Fit a circle to the trajectory and check direction
        traj = np.array(traj)
        x = traj[:,0]
        y = traj[:,1]
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        x_c = x - x_mean
        y_c = y - y_mean
        angles = np.arctan2(y_c, x_c)
        angle_diff = np.unwrap(np.diff(angles))
        total_angle = np.sum(angle_diff)
        if direction == 'cw' and total_angle > 3:
            return True
        if direction == 'ccw' and total_angle < -3:
            return True
        return False
