import pygame
import random
import sys
import os
import pygame.time
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('bgmusic.mp3')
correct_number_sound = pygame.mixer.Sound('ping.mp3')

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PASTEL_YELLOW = (255, 255, 153)  # Define PASTEL_YELLOW
GREEN = (0, 255, 0)
BRIGHT_GREEN = (0, 255, 0)
PIXELATED_FONT_FILE = os.path.join(os.path.dirname(__file__), 'Stepalange-x3BLm.otf')
FONT = pygame.font.Font(PIXELATED_FONT_FILE, 36)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5

# Falling numbers
falling_numbers = []

# Sequence
sequence = ['1', '0', '1', '0', '1', '0', '1']
sequence_colors = [WHITE] * len(sequence)  # Track the colors of the sequence

# Health bar
health = 100.0

# Speed reduction factor
speed_reduction_factor = 0.75

# Current index
current_index = 0

score = 0

completed_sequences = 0

# Completed sequences counter
completed_sequences_counter = 0

# Set the game duration to 1 minute and 30 seconds (in milliseconds)
GAME_DURATION = 90 * 1000  # 90 seconds
start_time = 0  # Variable to store the start time

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")
clock = pygame.time.Clock()

# Loads the BG Image
background_image = pygame.image.load('bg1.gif')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load the splash screen image
splash_screen_image = pygame.image.load('bgmenu.png')
splash_screen_image = pygame.transform.scale(splash_screen_image, (WIDTH, HEIGHT))

# Loads the Music for every completed sequence
pygame.mixer.music.play(-1)
sequence_complete_sound = pygame.mixer.Sound('sequenceComplete.mp3')


# Loads the sprites for the falling 1's and 0's
falling_image_1 = pygame.transform.scale(pygame.image.load('one.png'), (40, 40))
falling_image_0 = pygame.transform.scale(pygame.image.load('zero.png'), (40, 40))

idle_filenames = ["pescy_idle.png"]  # Add more filenames as needed
left_filenames = ["pescy_left_1.png", "pescy_left_2.png", "pescy_left_3.png", "pescy_left_4.png", "pescy_left_5.png", "pescy_left_6.png", "pescy_left_7.png"]  # Add more filenames as needed
right_filenames = ["pescy_right_1.png", "pescy_right_2.png", "pescy_right_3.png", "pescy_right_4.png", "pescy_right_5.png", "pescy_right_6.png", "pescy_right_7.png"]  # Add more filenames as needed

# Load frames
idle_frames = [pygame.image.load(filename) for filename in idle_filenames]
left_frames = [pygame.image.load(filename) for filename in left_filenames]
right_frames = [pygame.image.load(filename) for filename in right_filenames]

# Set initial frame index for each animation
current_frame_index_left = 0
current_frame_index_right = 0
current_frame_index_idle = 0

fun_fact_messages = [
    "Automatons are self-operating machines or control devices.",
    "The concept of automata dates back to ancient times.",
    "DFAs process inputs through states with transition rules.",
    "DFAs are used in lexical analysis and pattern matching in compilers and string processing algorithms.",
    "DFAs are deterministic, ensuring a unique state transition per input.",
    "The term 'automaton' is derived from the Greek word 'automatos', meaning self-moving.",
    "Automata theory is a fundamental concept in computer science.",
    "Turing machines, a type of automaton, influenced the concept of computation.",
    "Pushdown automata extend finite automata with a stack for added complexity.",
    "Cellular automata, like Conway's Game of Life, showcase emergent complexity through simple rules.",
    "The Jaquet-Droz 'The Writer'' automaton, created in the 18th century, is considered one of the most expensive automata.",
    "The Antikythera mechanism (200 BCE) is the oldest known automaton from ancient Greece."
]

random.shuffle(fun_fact_messages)

current_fun_fact_index = 0  # Keep track of the current fun fact index

last_fun_fact_change_time = pygame.time.get_ticks()




def splash_screen():
    while True:
        screen.blit(splash_screen_image, (0, 0))

        # Display "Click here to proceed" text
        draw_text(". . . .", WIDTH // 2 - 30, HEIGHT // 2 + 130, WHITE, highlighted=True)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 150 < x < WIDTH // 2 + 150 and HEIGHT // 2 < y < HEIGHT // 2 + 50:
                    return


def spawn_number():
    quantity = random.randint(1, 3)
    for _ in range(quantity):
        number = random.choice(['0', '1'])
        x = random.randint(0, WIDTH - player_size)
        y = 0
        falling_numbers.append({'number': number, 'x': x, 'y': y, 'highlighted': False})


def draw_text(text, x, y, color=WHITE, highlighted=False, font_size=36):
    font = pygame.font.Font(PIXELATED_FONT_FILE, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update_player_position():
    global player_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

def reset_game_state():
    global current_index, health, sequence, sequence_colors, speed_reduction_factor, score
    current_index = 0
    health = 100.0  # Reset health
    sequence = [random.choice(['0', '1']) for _ in range(len(sequence))]  # Generate a new sequence
    sequence_colors = [WHITE] * len(sequence)  # Reset sequence colors
    speed_reduction_factor = 0.75  # Reset speed reduction factor
    score += 100  # Increase the player's score (adjust the value as needed)

    # Play the sound effect
    sequence_complete_sound.play()


def defeated_menu():
    while True:
        screen.fill(BLACK)
        draw_text("You were defeated!", WIDTH // 2 - 150, HEIGHT // 2 - 50, RED)
        draw_text("Try again", WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text("Exit", WIDTH // 2 + 50, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 150 < x < WIDTH // 2 - 50 and HEIGHT // 2 + 50 < y < HEIGHT // 2 + 90:
                    reset_game_state()
                    return
                elif WIDTH // 2 + 50 < x < WIDTH // 2 + 100 and HEIGHT // 2 + 50 < y < HEIGHT // 2 + 90:
                    pygame.quit()
                    sys.exit()


def start_menu():
    # Load the start menu background image
    start_menu_bg = pygame.image.load('bgstart.png')  # Replace 'start_menu_bg.jpg' with your image file
    start_menu_bg = pygame.transform.scale(start_menu_bg, (WIDTH, HEIGHT))

    while True:
        # Draw the background image
        screen.blit(start_menu_bg, (0, 0))

        draw_text("Start Game", WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Instructions", WIDTH // 2, HEIGHT // 2)
        draw_text("Exit", WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 75 < x < WIDTH // 2 + 75 and HEIGHT // 2 - 75 < y < HEIGHT // 2 - 25:
                    return "start_game"
                elif WIDTH // 2 - 75 < x < WIDTH // 2 + 75 and HEIGHT // 2 - 25 < y < HEIGHT // 2 + 25:
                    return instructions_menu()  # Call instructions_menu instead of exiting the game
                elif WIDTH // 2 - 75 < x < WIDTH // 2 + 75 and HEIGHT // 2 + 25 < y < HEIGHT // 2 + 75:
                    pygame.quit()
                    sys.exit()

def instructions_menu():
    # Load the instructions background image
    instructions_bg = pygame.image.load('bgintro.png')  # Replace 'instructions_bg.jpg' with your image file
    instructions_bg = pygame.transform.scale(instructions_bg, (WIDTH, HEIGHT))

    while True:
        # Draw the instructions background image
        screen.blit(instructions_bg, (0, 0))

        # Calculate the horizontal and vertical positions to center the instructions
        text_x = (WIDTH - 600) // 2  # Adjust this value based on your preference
        text_y = (HEIGHT - 150) // 2  # Adjust this value based on your preference


        # Draw instructions text (you can customize this text based on your actual instructions)
        draw_text("Welcome to FinTomata! by Joaquin Tolentino", text_x - 50, text_y - 50, color=BLACK, font_size=30)
        draw_text("Use the left and right arrow keys to move Pescy the Fish!.", text_x - 50, text_y, color=BLACK, font_size=30)
        draw_text("Catch the falling numbers according to the Binary sequence", text_x - 50, text_y + 50, color=BLACK, font_size=30)
        draw_text("That shows up at the top left side of your screen. Remember!", text_x - 50, text_y + 100, color=BLACK, font_size=30)
        draw_text("Your Goal is to complete as many binary sequences as possible.", text_x - 50, text_y + 150, color=BLACK, font_size=30)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                return "start_menu"


def update_falling_numbers():
    global current_index, health, speed_reduction_factor
    for number in falling_numbers:
        number['y'] += int(5 * (1 + speed_reduction_factor))

        # Draw the appropriate image based on the falling number
        if number['number'] == '1':
            screen.blit(falling_image_1, (number['x'], number['y']))
        elif number['number'] == '0':
            screen.blit(falling_image_0, (number['x'], number['y']))

        # Check if the player caught the correct number
        if (
                player_x < number['x'] < player_x + player_size
                and player_y < number['y'] < player_y + player_size
        ):
            if number['number'] == sequence[current_index]:
                # Success: Highlight the correct next number
                number['highlighted'] = True
                sequence_colors[current_index] = GREEN  # Update color
                current_index += 1
                if current_index < len(sequence):
                    sequence_colors[current_index] = WHITE  # Set the next number to be highlighted
                else:
                    # If sequence is fulfilled, reset the game state
                    reset_game_state()
                    health += 25.0  # Regenerate 25% health

                correct_number_sound.play()  # Play the sound effect

            else:
                # Deduct 30% from health
                health -= 30.0
                speed_reduction_factor = max(0.5, speed_reduction_factor - 0.25)  # Reduce speed

            falling_numbers.remove(number)

def draw_sequence():
    sequence_height = 40  # Adjust this value based on how much lower you want the sequence
    for i, (digit, color) in enumerate(zip(sequence, sequence_colors)):
        draw_text(digit, 10 + i * 30, 30 + sequence_height, color)

def draw_health_bar():
    health_bar_width = int(health * 2)
    health_bar_x = WIDTH - health_bar_width - 10
    pygame.draw.rect(screen, RED, (health_bar_x, 10, health_bar_width, 20))
    pygame.draw.rect(screen, GREEN, (health_bar_x, 10, int(health * 2), 20))



def game():
    global player_x, falling_numbers, health, speed_reduction_factor, current_frame_index_left, current_frame_index_right, current_frame_index_idle, start_time, completed_sequences_counter, current_fun_fact_index

    pygame.mixer.music.play(-1)

    # Set the initial direction
    current_direction = 'idle'

    # Initialize the start time when the game begins
    start_time = pygame.time.get_ticks()

    while True:
        screen.blit(background_image, (0, 0))

        handle_events()

        # Check if the escape key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            reset_game_state()
            completed_sequences_counter = 0
            return "start_menu"

        update_player_position()
        update_falling_numbers()

        # Check if health is 0
        if health <= 0:
            pygame.mixer.music.pause()  # Pause background music
            defeated_menu()

        # Determine the current direction based on player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            current_direction = 'left'
        elif keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            current_direction = 'right'
        else:
            current_direction = 'idle'

        # Spawn new numbers
        if random.randint(0, 100) < 5:
            spawn_number()

        # Draw player with the current frame based on the current direction
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        if current_direction == 'left':
            frames_to_use = left_frames
            current_frame_index = current_frame_index_left
        elif current_direction == 'right':
            frames_to_use = right_frames
            current_frame_index = current_frame_index_right
        else:
            frames_to_use = idle_frames
            current_frame_index = current_frame_index_idle

        screen.blit(frames_to_use[current_frame_index], player_rect)

        # Draw sequence
        draw_sequence()

        # Draw health bar (moved to top right)
        draw_text("Health:", WIDTH - 400, 10)
        draw_health_bar()

        # Draw timer
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, (GAME_DURATION - elapsed_time) // 1000)  # Convert to seconds
        draw_text(f"Time: {remaining_time // 60:02}:{remaining_time % 60:02}", 10, 10)

        # Check if the timer has expired
        if elapsed_time >= GAME_DURATION:
            # Game over - show score and congratulations
            pygame.mixer.music.pause()  # Pause background music
            screen.fill(BLACK)
            draw_text(f"Congratulations!", WIDTH // 2 - 150, HEIGHT // 2 - 50, BRIGHT_GREEN)
            draw_text(f"Score: {completed_sequences_counter}", WIDTH // 2 - 150, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(5000)  # Display for 5 seconds
            reset_game_state()
            completed_sequences_counter = 0
            return "start_menu"

        # Update frame index for the current direction
        if current_direction == 'left':
            current_frame_index_left = (current_frame_index_left + 1) % len(left_frames)
        elif current_direction == 'right':
            current_frame_index_right = (current_frame_index_right + 1) % len(right_frames)
        else:
            current_frame_index_idle = (current_frame_index_idle + 1) % len(idle_frames)

        # Draw the fun fact message
        draw_fun_fact()

        scroll_offset = draw_fun_fact()

        pygame.display.flip()
        clock.tick(FPS)

        # Reset game state after drawing health bar
        if current_index == len(sequence):
            reset_game_state()
            completed_sequences_counter += 1


def draw_fun_fact():
    global current_fun_fact_index, last_fun_fact_change_time

    fun_fact_message = fun_fact_messages[current_fun_fact_index]
    current_time = pygame.time.get_ticks()

    # Calculate scrolling offset based on time difference
    scroll_offset = (current_time - last_fun_fact_change_time) // 8 % (
                len(fun_fact_message) * 25)  # Adjust scrolling speed
    scrolled_message = fun_fact_message + "                   " * 10  # Add extra spaces for smoother scrolling

    # Draw scrolling text at a lower position
    draw_text(scrolled_message, WIDTH - scroll_offset, 200, BLACK, font_size=25)

    # Check if a complete scrolling cycle has occurred
    if scroll_offset == 0:
        # Change the fun fact
        current_fun_fact_index = (current_fun_fact_index + 1) % len(fun_fact_messages)
        last_fun_fact_change_time = current_time



if __name__ == "__main__":
    splash_screen()

    menu_choice = "start_menu"

    while True:
        if menu_choice == "start_menu":
            menu_choice = start_menu()
        elif menu_choice == "start_game":
            menu_choice = game()
        elif menu_choice == "instructions":
            # Handle instructions screen (you can add instructions logic here)
            menu_choice = "start_menu"