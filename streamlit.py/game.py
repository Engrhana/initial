import streamlit as st
import random
import time

# Function to initialize the game
def initialize_game():
    images = ["🐶", "🐱", "🐰", "🐻", "🦁", "🐸", "🐷", "🐵"] * 2  # Duplicate emojis for pairs
    random.shuffle(images)
    return {
        "cards": images,
        "flipped": [False] * len(images),
        "matches": 0,
        "first_card": None,
        "second_card": None,
        "turns": 0,
        "time_limit": 60,  # Set time limit in seconds
        "start_time": time.time()  # Record the start time
    }

# Function to check for matches
def check_for_match(game_state):
    if game_state['first_card'] is not None and game_state['second_card'] is not None:
        if game_state['cards'][game_state['first_card']] == game_state['cards'][game_state['second_card']]:
            game_state['matches'] += 1
        else:
            # Delay to show the second card before flipping back
            time.sleep(1)
            game_state['flipped'][game_state['first_card']] = False
            game_state['flipped'][game_state['second_card']] = False
        game_state['first_card'] = None
        game_state['second_card'] = None
        game_state['turns'] += 1

# Main game function
def main():
    st.title("Memory Puzzle Game")

    if 'game_state' not in st.session_state:
        st.session_state.game_state = initialize_game()

    game_state = st.session_state.game_state

    # Calculate remaining time
    elapsed_time = time.time() - game_state['start_time']
    remaining_time = game_state['time_limit'] - elapsed_time

    if remaining_time <= 0:
        st.write("Time's up! Game over!")
        st.stop()  # Stop the game if time is up

    # Display remaining time
    st.write(f"Time remaining: {int(remaining_time)} seconds")

    # Display cards
    cols = st.columns(4)  # Adjust based on the number of cards
    for i in range(len(game_state['cards'])):
        if game_state['flipped'][i]:
            cols[i % 4].write(game_state['cards'][i])
        else:
            if cols[i % 4].button("Flip", key=i):
                if game_state['first_card'] is None:
                    game_state['first_card'] = i
                elif game_state['second_card'] is None:
                    game_state['second_card'] = i
                game_state['flipped'][i] = True

                # Check for matches after two cards are flipped
                if game_state['first_card'] is not None and game_state['second_card'] is not None:
                    check_for_match(game_state)

    # Display matches found and turns taken
    st.write(f"Matches found: {game_state['matches']}")
    st.write(f"Turns taken: {game_state['turns']}")

    # Congratulate player if they completed the game in time
    if game_state['matches'] == len(game_state['cards']) // 2 and remaining_time > 0:
        st.success("Congratulations! You've completed the game in time!")

    # Restart game button
    if st.button("Restart Game"):
        st.session_state.game_state = initialize_game()

if __name__ == "_main_":
    main()