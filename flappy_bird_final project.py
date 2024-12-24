import tkinter as tk
import random

# Set up the main window
WIDTH = 850
HEIGHT = 750
window = tk.Tk()
window.title("Flappy Bird")
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# Load the bird image
bird_image = tk.PhotoImage(file="bird.png")  # Ensure bird.png is in the same directory
bird_width = bird_image.width()
bird_height = bird_image.height()

# Game variables
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

pipe_width = 60
pipe_gap = 150
pipe_speed = 5
score = 0
highest_score = 0
level = 1
pipes = []
pipe_passed = 0

# Create the bird using the image
bird = canvas.create_image(bird_x, bird_y, anchor="nw", image=bird_image)

# Function to generate pipes
def create_pipe():
    top_height = random.randint(50, HEIGHT - pipe_gap - 50)
    bottom_height = HEIGHT - pipe_gap - top_height
    top_pipe = canvas.create_rectangle(WIDTH, 0, WIDTH + pipe_width, top_height, fill="green")
    bottom_pipe = canvas.create_rectangle(WIDTH, HEIGHT - bottom_height, WIDTH + pipe_width, HEIGHT, fill="green")
    return (top_pipe, bottom_pipe)  # Return a tuple

# Create the initial pipes
pipes.append(create_pipe())  # Append the tuple to the pipes list

# Function to move pipes
def move_pipes():
    global score, pipe_passed, level, pipe_speed, pipe_gap
    for top_pipe, bottom_pipe in pipes:
        canvas.move(top_pipe, -pipe_speed, 0)
        canvas.move(bottom_pipe, -pipe_speed, 0)

    # Remove pipes that have moved off-screen and add new ones
    if canvas.coords(pipes[0][0])[2] < 0:
        canvas.delete(pipes[0][0])
        canvas.delete(pipes[0][1])
        pipes.pop(0)
        pipes.append(create_pipe())

        # Increment score and adjust difficulty
        pipe_passed += 1
        if pipe_passed >= 1:
            score += 1
            pipe_passed = 0
            # Adjust difficulty as score increases
            if score % 5 == 0:
                level += 1
                pipe_speed += 1
                if pipe_gap > 100:
                    pipe_gap -= 10

# Function to handle jumping
def jump(event):
    global bird_velocity
    bird_velocity = jump_strength

# Function to update the game state
def update_game():
    global bird_y, bird_velocity, pipes, score, pipe_passed, highest_score, level

    # Apply gravity
    bird_velocity += gravity
    bird_y += bird_velocity

    # Update the bird position
    canvas.coords(bird, bird_x, bird_y)

    # Move pipes
    move_pipes()

    # Collision detection with pipes
    for top_pipe, bottom_pipe in pipes:
        pipe_coords_top = canvas.coords(top_pipe)
        pipe_coords_bottom = canvas.coords(bottom_pipe)

        # Check for collision with top pipe
        if (pipe_coords_top[0] < bird_x + bird_width and pipe_coords_top[2] > bird_x and
            bird_y < pipe_coords_top[3] and bird_y + bird_height > pipe_coords_top[1]):
            game_over()
            return

        # Check for collision with bottom pipe
        if (pipe_coords_bottom[0] < bird_x + bird_width and pipe_coords_bottom[2] > bird_x and
            bird_y + bird_height > pipe_coords_bottom[1] and bird_y < pipe_coords_bottom[3]):
            game_over()
            return

    # Collision detection with the ground and ceiling
    if bird_y <= 0 or bird_y + bird_height >= HEIGHT:
        game_over()
        return

    # Update score and level on the canvas
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(level_text, text=f"Level: {level}")

    # Update the game every 20ms
    window.after(20, update_game)

# Game over function
def game_over():
    global highest_score, score
    if score > highest_score:
        highest_score = score  # Update highest score if current score is higher

    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", font=("Arial", 30), fill="red")
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text=f"Final Score: {score}", font=("Arial", 20), fill="red")
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 80, text="Press 'R' to Restart", font=("Arial", 14), fill="blue")

    # Bind the 'R' key to restart the game
    window.bind("<r>", restart_game)

# Restart the game function
def restart_game(event):
    global score, bird_y, bird_velocity, pipes, pipe_passed, level, pipe_speed, pipe_gap
    # Reset game variables
    score = 0
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    pipe_passed = 0
    level = 1
    pipe_speed = 4
    pipe_gap = 150

    # Clear the canvas
    canvas.delete("all")

    # Recreate the bird and score display
    global bird, score_text, level_text
    bird = canvas.create_image(bird_x, bird_y, anchor="nw", image=bird_image)
    score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 14), fill="white")
    level_text = canvas.create_text(10, 30, anchor="nw", text=f"Level: {level}", font=("Arial", 14), fill="white")

    # Create the initial pipes
    pipes.append(create_pipe())

    # Restart the game loop
    update_game()

# Draw initial score and level on canvas
score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 14), fill="white")
level_text = canvas.create_text(10, 30, anchor="nw", text=f"Level: {level}", font=("Arial", 14), fill="white")

# Bind the jump function to the spacebar
window.bind("<space>", jump)

# Start the game
update_game()

# Run the game loop
window.mainloop()
