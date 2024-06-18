import pygame
import sys
import math
import cv2
import numpy as np
import mediapipe as mp
from finish_screen import finish

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

dis_width = 1280
dis_height = 720

# Sine curve properties
amplitude = 100  # Amplitude of the sine wave
frequency = 0.01  # Frequency of the sine wave
offset_x = 0  # Initial offset from the left edge of the screen
offset_y = dis_height // 1.5  # Vertical center of the screen
line_speed = 10 # Initial speed of the sine curves

# Time variables for gameplay
start_time = 0
time_elapsed = 0
game_started = False


# Create the display
dis = pygame.display.set_mode((dis_width, dis_height))

# Set up the initial clock tick rate
tick_rate = 60

# Set up the clock
clock = pygame.time.Clock()

# Time variables for speeding up every 5 seconds
SPEED_UP_TIME = 5000  # Time interval to speed up (5 seconds in milliseconds)

# Total duration for the animation (60 seconds)
ANIMATION_DURATION = 60000  # 60 seconds in milliseconds

# Initialize OpenCV and Mediapipe

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Scoring variables
score = 0
increase_score = 1  # Score increment when between curves
decrease_penalty = 1  # Score decrement when outside curves

# Countdown variables
countdown_start_time = pygame.time.get_ticks()
countdown_duration = 3000  # 3 seconds in milliseconds
countdown_font = pygame.font.SysFont(None, 200)
countdown_text = ""

def draw_nose(frame, landmarks):
    # Get the coordinates of the nose
    nose = landmarks.landmark[mp_pose.PoseLandmark.NOSE]
    nose_x = int(nose.x * dis_width)
    nose_y = int(nose.y * dis_height)
    return nose_x, nose_y

def check_collision(nose_x, nose_y, points1, points2):
    if 0 <= nose_x < len(points1):
        y1 = points1[nose_x][1]
        y2 = points2[nose_x][1]
        
        # Check if nose_y is between y1 and y2
        if y2 < nose_y < y1:
            return 'increase'  # Increase score if nose is between y1 and y2
        else:
            return 'decrease'  # Decrease score if nose is above y2 or below y1

    return 'decrease'  # Default to decrease if nose_x is out of bounds

def draw_countdown():
    """Draw the countdown text on the screen."""
    if pygame.time.get_ticks() - countdown_start_time < countdown_duration:
        countdown_time_left = 3 - (pygame.time.get_ticks() - countdown_start_time) // 1000
        countdown_text = str(countdown_time_left) if countdown_time_left > 0 else "Go!"
        text_surface = countdown_font.render(countdown_text, True, white)
        text_rect = text_surface.get_rect(center=(dis_width // 2, dis_height // 2))
        dis.blit(text_surface, text_rect)

def draw_time_remaining():
    global game_started, start_time
    
    """Draw the time remaining during gameplay."""
    if game_started:
        time_remaining = max(0, (ANIMATION_DURATION - (pygame.time.get_ticks() - start_time)) // 1000)
        font = pygame.font.Font("/Users/pongsakorn/Documents/draft999/assets/font.ttf", 30)
        text = font.render(f"Time: {time_remaining} seconds", True, blue)
        dis.blit(text, (dis_width - 300, 10))

score_delay = 0

# Main game loop

def hardgame(window, manager, clock, name, mode):
    global game_started, start_time
    
    # Sine curve properties
    amplitude = 100  # Amplitude of the sine wave
    frequency = 0.01  # Frequency of the sine wave
    offset_x = 0  # Initial offset from the left edge of the screen
    offset_y = dis_height // 1.5  # Vertical center of the screen
    line_speed = 10 # Initial speed of the sine curves
    
    # Time variables for gameplay
    start_time = 0
    time_elapsed = 0
    game_started = False
    
    cap = cv2.VideoCapture(0)
    
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe Pose
        results = pose.process(frame_rgb)

        # Convert the frame to a Pygame surface
        frame_rgb = cv2.resize(frame_rgb, (dis_width, dis_height))
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.rotate(frame_surface, -90)
        frame_surface = pygame.transform.flip(frame_surface, True, False)

        # Move the sine curves to the left
        offset_x -= line_speed  # Decrement offset_x to move to the left

        # Wrap around logic
        if offset_x < -dis_width:  # Reset offset_x when it goes off the left edge
            roffset_x = 0

        # Draw the video frame
        dis.blit(frame_surface, (0, 0))

        # Draw the sine curves
        points1 = []
        points2 = []
        for x in range(dis_width):
            # Calculate y-coordinates for the sine curves
            y1 = int(offset_y + amplitude * math.sin(frequency * (x - offset_x)))  # Subtract offset_x to move to the left
            y2 = int(0.75 * offset_y + amplitude * math.sin(frequency * (x - offset_x)))  # Subtract offset_x to move to the left

            # Add points to the lists for drawing
            points1.append((x, y1))
            points2.append((x, y2))

        # Draw the sine curves
        pygame.draw.lines(dis, green, False, points1, 3)
        pygame.draw.lines(dis, green, False, points2, 3)

        # Draw the nose landmark if detected
        if results.pose_landmarks:
            nose_x, nose_y = draw_nose(frame, results.pose_landmarks)
            collision_result = check_collision(nose_x, nose_y, points1, points2)
            if collision_result == 'increase':
                score += increase_score
            elif collision_result == 'decrease':
                score -= decrease_penalty

            # Draw nose dot
            pygame.draw.circle(dis, red, (nose_x, nose_y), 10)

        # Display score
        # if game_started and pygame.time.get_ticks() - start_time >= score_delay:
        #     font = pygame.font.SysFont(None, 36)
        #     text = font.render(f"Score: {score}", True, white)
        #     dis.blit(text, (10, 10))

        # Draw countdown on the screen
        draw_countdown()

        # Draw time remaining on the screen
        draw_time_remaining()

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clock.tick(tick_rate)

        # Check if countdown has finished
        if pygame.time.get_ticks() - countdown_start_time >= countdown_duration and not game_started:
            # Start gameplay timer
            start_time = pygame.time.get_ticks()
            game_started = True

        # Update elapsed time
        time_elapsed = pygame.time.get_ticks() - start_time

        # Speed up the sine curve every 5 seconds
        if game_started and (time_elapsed // SPEED_UP_TIME > (time_elapsed - clock.get_time()) // SPEED_UP_TIME):
            line_speed += 2  # Increase the speed by 2 units every 5 seconds

        # Check if game time is over
        if time_elapsed >= ANIMATION_DURATION:
            finish(name, mode, score)
            
    # Release the capture and close the window
    cap.release()  



