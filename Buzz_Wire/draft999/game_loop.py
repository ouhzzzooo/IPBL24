import pygame
import cv2
import numpy as np
import mediapipe as mp
import math
import sys
import time
from utils import get_font
from main2 import window_width, window_height
from finish_screen import finish
from main2 import ending_tt

def detect_hand_position(cap, mp_hands, hands, detection_enabled):
    ret, frame = cap.read()
    if not ret:
        return None, frame
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    

    hand_pos = None
    if results.multi_hand_landmarks and detection_enabled:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_pos = hand_landmarks.landmark[8]
            hand_pos = (1280 - int(hand_pos.x * window_width), int(hand_pos.y * window_height))
            break

    return hand_pos, frame

def game_loop(window, manager, clock, name, mode, start_tt):
    
    ring_pos = [50, 450]
    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    ring_radius = 20
    ring_color = (0, 0, 255)

    points_1 = [(100, 525), (540, 610), (250, 160), (590, 110)]
    points_2= [(100, 460), (540, 520), (100, 40), (590, 40)]
    
    points_3 = [(590, 40), (1080, 0), (540, 720), (1180, 530)]
    points_4 = [(590, 110), (900, 130), (520, 700), (1180, 622)]

    def bezier_curve(t, points):
        x = (1-t)**3 * points[0][0] + 3 * (1-t)**2 * t * points[1][0] + 3 * (1-t) * (t**2) * points[2][0] + t**3 * points[3][0]
        y = (1-t)**3 * points[0][1] + 3 * (1-t)**2 * t * points[1][1] + 3 * (1-t) * (t**2) * points[2][1] + t**3 * points[3][1]
        return (x, y)

    detection_enabled = True
    pause_time = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if pause_time and time.time() - pause_time > 3:
            detection_enabled = True
            pause_time = None
            ring_pos = [50, 450]
            ring_color = (0, 0, 255)

        hand_pos, frame = detect_hand_position(cap, mp_hands, hands, detection_enabled)
        if hand_pos:
            ring_pos = list(hand_pos)

        frame = cv2.resize(frame, (window_width, window_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        window.blit(frame, (0, 0))
        
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect(0, 0, 100, 720), 2)
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(1180, 0, 100, 720), 2)
        pygame.draw.circle(window, ring_color, ring_pos, ring_radius, 5)
        
        for t in range(0, 101):
            t /= 100
            pos = bezier_curve(t, points_1)
            pygame.draw.circle(window, (34, 139, 34), (int(pos[0]), int(pos[1])), 5)

        for t in range(0, 101):
            t /= 100
            pos = bezier_curve(t, points_2)
            pygame.draw.circle(window, (34, 139, 34), (int(pos[0]), int(pos[1])), 5)
            
        for t in range(0, 101):
            t /= 100
            pos = bezier_curve(t, points_3)
            pygame.draw.circle(window, (34, 139, 34), (int(pos[0]), int(pos[1])), 5)
            
        for t in range(0, 101):
            t /= 100
            pos = bezier_curve(t, points_4)
            pygame.draw.circle(window, (34, 139, 34), (int(pos[0]), int(pos[1])), 5)

        for t in range(0, 101):
            t /= 100
            curve_pos1 = bezier_curve(t, points_1)
            distance1 = math.sqrt((int(curve_pos1[0]) - ring_pos[0]) ** 2 + (int(curve_pos1[1]) - ring_pos[1]) ** 2)
            if distance1 < ring_radius:
                ring_color = (240, 128, 128)
                detection_enabled = False
                pause_time = time.time()
                ring_pos = [50, 450]
                break
            
        for t in range(0, 101):
            t /= 100
            curve_pos2 = bezier_curve(t, points_2)
            distance2 = math.sqrt((int(curve_pos2[0]) - ring_pos[0]) ** 2 + (int(curve_pos2[1]) - ring_pos[1]) ** 2)
            if distance2 < ring_radius:
                ring_color = (240, 128, 128)
                detection_enabled = False
                pause_time = time.time()
                ring_pos = [50, 450]
                
        for t in range(0, 101):
            t /= 100
            curve_pos2 = bezier_curve(t, points_3)
            distance2 = math.sqrt((int(curve_pos2[0]) - ring_pos[0]) ** 2 + (int(curve_pos2[1]) - ring_pos[1]) ** 2)
            if distance2 < ring_radius:
                ring_color = (240, 128, 128)
                detection_enabled = False
                pause_time = time.time()
                ring_pos = [50, 450]
                
        for t in range(0, 101):
            t /= 100
            curve_pos2 = bezier_curve(t, points_4)
            distance2 = math.sqrt((int(curve_pos2[0]) - ring_pos[0]) ** 2 + (int(curve_pos2[1]) - ring_pos[1]) ** 2)
            if 1180 <= ring_pos[0] <= 1280 and 530 <= ring_pos[1] <= 622:
                end_tt = ending_tt()
                score = 2000 - (end_tt - start_tt) //100
                finish(name, mode, score)
            if distance2 < ring_radius:
                ring_color = (240, 128, 128)
                detection_enabled = False
                pause_time = time.time()
                ring_pos = [50, 450]
                break
        
        pygame.display.update()

    cap.release()

