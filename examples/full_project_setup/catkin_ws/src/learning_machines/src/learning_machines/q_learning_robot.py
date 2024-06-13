
# Task-1: Obstacle avoidance

# The specific task or challenge is:
# The robot should displace in the environment as further and as fast as possible with minimal collision.


import pickle
import numpy as np
import os


from data_files import FIGRURES_DIR
from robobo_interface import (
    IRobobo,
    Emotion,
    LedId,
    LedColor,
    SoundEmotion,
    SimulationRobobo,
    HardwareRobobo,
)

# Define the actions
actions = ['forward', 'left', 'right', 'slight_left', 'slight_right']


def initialize_q_table(file_path='q_table.pkl', num_bins=4, num_sensors=3):
    """Load the Q-table from a file if it exists; otherwise, initialize a new Q-table with small random values."""
    """Initialize the Q table instead of zeros with small random values to encourage initial exploration."""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            q_table = pickle.load(f)
    else:
        num_states = num_bins ** num_sensors
        num_actions = len(actions)
        q_table = np.random.uniform(low=0, high=1, size=(num_states, num_actions))
        save_q_table(q_table, file_path)  # Save the new Q-table for the first time
    return q_table
    
    
def load_q_table(file_path='q_table.pkl'):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
    
def save_q_table(q_table, file_path='q_table.pkl'):
    with open(file_path, 'wb') as f:
        pickle.dump(q_table, f)


def get_epsilon(episode, min_epsilon=0.01, decay=0.99):
    """Calculate epsilon based on the current episode using exponential decay."""
    return max(min_epsilon, decay ** episode)


def choose_action(state, q_table, epsilon=0.1):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(len(actions))
    else:
        return np.argmax(q_table[state])


def get_state_from_ir_values(ir_values, num_bins=4, num_sensors=3):
    def bin_value(value):
        if value == float('inf'):
            return 0  # No detection or sensor error
        elif value < 6:
            return 0  # No detection
        elif value < 10:
            return 1  # Detected 
        elif value <= 15:
            return 2  # Detected close
        else:
            return 3  # Hits object
    
    binned_values = [bin_value(value) for value in ir_values]
    state_index = sum(value * (num_bins ** i) for i, value in enumerate(binned_values))
    return state_index


def navigate_with_q_learning(rob, q_table_file='q_table.pkl'):
    q_table = load_q_table(q_table_file)  # Load the trained Q-table
    
    if isinstance(rob, SimulationRobobo): 
        rob.play_simulation()

    ir_values = rob.read_irs()
    selected_values = ir_values[4:6] + [ir_values[7]]
    state = get_state_from_ir_values(selected_values)

    while True:
        action_index = choose_action(state, q_table)
        action = actions[action_index]

        if action == 'forward':
            rob.move(50, 50, 1000)
        elif action == 'left':
            rob.move(0, 50, 500)
        elif action == 'right':
            rob.move(50, 0, 500)
        elif action == 'slight_left':
            rob.move(25, 50, 500)
        elif action == 'slight_right':
            rob.move(50, 25, 500)
        rob.sleep(0.1)

        ir_values = rob.read_irs()
        selected_values = ir_values[4:6] + [ir_values[7]]

        print(selected_values)

        if any(value > 15 and value < 1500 for value in selected_values): 
            print("Hit")
            break
    
    if isinstance(rob, SimulationRobobo):
        rob.stop_simulation()
    

def simulate_robot_action(rob, action=None):
    """Simulate the robot action and compute the reward and next state."""
    if action == 'forward':
        rob.move_blocking(50, 50, 1000)
        movement_cost = 1
    elif action == 'left' or action == 'right':
        rob.move_blocking(0, 50, 500) if action == 'left' else rob.move_blocking(50, 0, 500)
        movement_cost = 2
    elif action == 'slight_left' or action == 'slight_right':
        rob.move_blocking(25, 50, 500) if action == 'slight_left' else rob.move_blocking(50, 25, 500)
        movement_cost = 1.5
    rob.sleep(0.1)

    ir_values = rob.read_irs()
    selected_values = ir_values[4:6] + [ir_values[7]]
    next_state = get_state_from_ir_values(selected_values)
    
    if any(value > 15 and value < 1500 for value in selected_values):    
        reward = -50  # Penalty for hitting an object
    else:
        reward = 1 - movement_cost  # Reward for moving safely, penalize based on movement cost

    return next_state, reward


def train_q_table(rob, q_table, num_episodes=2, max_steps=100, alpha=0.1, gamma=0.9, initial_epsilon=1.0):
    for episode in range(num_episodes):
        # Reset the environment and get the initial state
        if isinstance(rob, SimulationRobobo): 
            rob.play_simulation()
            print("Start simulation: ", episode)

        epsilon = get_epsilon(episode, decay=0.995)  # Update epsilon each episode
        ir_values = rob.read_irs()
        selected_values = ir_values[4:6] + [ir_values[7]]

        step = 0

        state = get_state_from_ir_values(selected_values)

        done = False
        while not done:
            try:
                # Choose an action using epsilon-greedy policy
                action_index = choose_action(state, q_table, epsilon)
                action = actions[action_index]

                # Take the action and observe the next state and reward
                next_state, reward = simulate_robot_action(rob, action)
                print("Next state:", next_state, "Reward:", reward)  # Debug statement

                # Update the Q-table
                best_next_action = np.argmax(q_table[next_state])
                q_table[state][action_index] += alpha * (reward + gamma * q_table[next_state][best_next_action] - q_table[state][action_index])
                
                state = next_state

                step += 1
                print("Episode: ", episode, "Step: ", step)
                if reward == -50 or step >= max_steps: #or next_state == 0:
                    done = True
                    if isinstance(rob, SimulationRobobo):
                        rob.stop_simulation()

            except Exception as e:
                print("An error occurred:", e)
                done = True  # End the episode if an error occurs
                if isinstance(rob, SimulationRobobo):
                    rob.stop_simulation()


    # Save the trained Q-table
    save_q_table(q_table)