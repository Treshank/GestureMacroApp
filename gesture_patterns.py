# gesture_patterns.py
# Utility for gesture pattern matching based on MediaPipe hand landmarks

import numpy as np

def is_peace(lm):
    # Peace sign: index and middle up, ring and pinky down
    # lm: list of 21 landmarks
    # y: lower value is higher on image (hand up)
    return (
        lm[8].y < lm[5].y and  # index tip above index base
        lm[12].y < lm[9].y and # middle tip above middle base
        lm[16].y > lm[13].y and # ring tip below ring base
        lm[20].y > lm[17].y    # pinky tip below pinky base
    )

def is_rock(lm):
    # Rock sign: thumb and pinky up, index, middle, ring down
    return (
        lm[4].y < lm[0].y and  # thumb tip above wrist
        lm[8].y < lm[5].y and  # index tip below index base
        lm[12].y > lm[9].y and # middle tip below middle base
        lm[16].y > lm[13].y and # ring tip below ring base
        lm[20].y < lm[17].y    # pinky tip above pinky base
    )



def is_finger_open(lm, tip, base):
    # Check if a finger is open based on its tip and base landmarks
    v_finger = np.array([lm[tip].x - lm[0].x, lm[tip].y - lm[0].y])
    v_base = np.array([lm[base].x - lm[0].x, lm[base].y - lm[0].y])
    dot = np.dot(v_finger, v_base)
    return dot > 0 and np.linalg.norm(v_finger) > np.linalg.norm(v_base)

def is_open_palm(lm):
    # All fingers up, considering hand tilt using vectors
    return (
        is_finger_open(lm, 8, 5) and
        is_finger_open(lm, 12, 9) and
        is_finger_open(lm, 16, 13) and
        is_finger_open(lm, 20, 17)
    )

def is_open_index(lm):
    # Only index finger open, others closed
    return (
        is_finger_open(lm, 8, 5) and
        not is_finger_open(lm, 12, 9) and
        not is_finger_open(lm, 16, 13) and
        not is_finger_open(lm, 20, 17)
    )

def is_fist(lm):
    # All fingers down
    return (
        lm[8].y > lm[6].y and
        lm[12].y > lm[10].y and
        lm[16].y > lm[14].y and
        lm[20].y > lm[18].y
    )

# Add more patterns as needed
