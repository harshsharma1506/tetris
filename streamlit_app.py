import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Constants
GRID_SIZE = 10
SHAPES = {
    'Square': np.array([[1, 1],
                        [1, 1]]),
    'L-shape': np.array([[1, 0],
                         [1, 0],
                         [1, 1]]),
    'T-shape': np.array([[0, 1, 0],
                         [1, 1, 1]]),
    'Line': np.array([[1, 1, 1, 1]]),
}

# Initialize the grid and color array
def create_grid():
    return np.zeros((GRID_SIZE, GRID_SIZE)), np.ones((GRID_SIZE, GRID_SIZE, 3))  # Color initialized to white

# Draw the grid with colors and grid lines
def draw_grid(grid, colors):
    plt.figure(figsize=(6, 6))
    plt.imshow(colors, vmin=0, vmax=1)  # Display color grid
    plt.xticks([])
    plt.yticks([])

    # Add grid lines for the overall grid
    for i in range(GRID_SIZE + 1):
        plt.axhline(i - 0.5, color='black', linewidth=1)
        plt.axvline(i - 0.5, color='black', linewidth=1)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i, j] == 1:
                plt.gca().add_patch(plt.Rectangle((j, i), 1, 1, color=colors[i, j]))

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')  # Hide axes for a cleaner look
    st.pyplot(plt)

def can_place_shape(grid, shape, position):
    x, y = position
    if (x + shape.shape[0] > GRID_SIZE) or (y + shape.shape[1] > GRID_SIZE):
        return False
    return np.all(grid[x:x + shape.shape[0], y:y + shape.shape[1]] + shape <= 1)

def place_shape(grid, shape, position):
    x, y = position
    grid[x:x + shape.shape[0], y:y + shape.shape[1]] += shape
    return grid

def generate_random_color():
    return np.random.rand(3)  # Random RGB color

def check_game_over(grid):
    return np.any(grid[0, :] > 0)  # Check if the first row is filled

# Function to generate a random math question
def generate_math_question():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    if operation == '+':
        answer = a + b
    elif operation == '-':
        answer = a - b
    else:
        answer = a * b
    return f"What is {a} {operation} {b}?", answer

def main():
    st.title("Trippy Fuckin' Tetris 🕹️")
    
    # Add GitHub link in the header
    st.markdown("[Meet the Dev](https://github.com/your-github-username/your-repo-name)")

    # Initialize game state
    if 'grid' not in st.session_state:
        st.session_state.grid, st.session_state.colors = create_grid()
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.drop_count = 0  # Count of shapes dropped

    # Draw the grid
    draw_grid(st.session_state.grid, st.session_state.colors)

    # Check for game over
    if check_game_over(st.session_state.grid):
        st.session_state.game_over = True

    # Display game over message if applicable
    if st.session_state.game_over:
        st.error("Game Over! The shapes have reached the top of the grid.")
        if st.button("Quit"):
            st.session_state.clear()  # Clear session state to reset the game
        return  # Exit the game loop

    # Display score
    st.write(f"Score: {st.session_state.score}")

    # Create buttons for dropping shapes at specific coordinates
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            with cols[j]:
                if st.button(f"({i}, {j})", key=f"button_{i}_{j}"):
                    # Select a random shape
                    selected_shape = random.choice(list(SHAPES.values()))
                    # Attempt to drop the shape
                    if can_place_shape(st.session_state.grid, selected_shape, (i, j)):
                        st.session_state.grid = place_shape(st.session_state.grid, selected_shape, (i, j))
                        color = generate_random_color()
                        # Place the color on the grid
                        for x in range(selected_shape.shape[0]):
                            for y in range(selected_shape.shape[1]):
                                if selected_shape[x, y] == 1:
                                    st.session_state.colors[i + x, j + y] = color
                        st.session_state.drop_count += 1  # Increment drop count

                        # Randomly prompt math question after every 5 drops
                        if st.session_state.drop_count % 5 == 0:
                            question, correct_answer = generate_math_question()
                            user_answer = st.number_input(question, min_value=0, max_value=100, step=1, key=f"math_q_{st.session_state.drop_count}")
                            if user_answer == correct_answer:
                                st.success("Correct answer! Keep playing.")
                            elif user_answer != 0:  # Only respond to non-zero inputs
                                st.error("Wrong answer! Game reset.")
                                st.session_state.grid, st.session_state.colors = create_grid()  # Reset the game

    # Check for game over after placing the shape
    if check_game_over(st.session_state.grid):
        st.session_state.game_over = True

    # Quit button
    if st.button("Quit"):
        st.session_state.clear()  # Clear session state to reset the game

if __name__ == "__main__":
    main()
