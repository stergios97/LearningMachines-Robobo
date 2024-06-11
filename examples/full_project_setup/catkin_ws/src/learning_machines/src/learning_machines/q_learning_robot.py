
# Task-1: Obstacle avoidance

# The specific task or challenge is:
# The robot should displace in the environment as further and as fast as possible with minimal collision.


import pickle
import numpy as np
import os

# from data_files import FIGRURES_DIR
from robobo_interface import SimulationRobobo

# Defining the Environment
# 1. Actions
# 2. States
# 3. Rewards

actions = ['forward', 'left', 'right', 'slight_left', 'slight_right']

def initialize_q_table(file_path = 'q_table.pkl', num_bins = 5, num_sensors = 5):
    """Load the Q-table from a file if it exists; otherwise, initialize a new Q-table."""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            q_table = pickle.load(f)
    else:
        num_states = num_bins ** num_sensors
        num_actions = len(actions)
        q_table = np.zeros((num_states, num_actions))
        save_q_table(q_table, file_path)  # Save the new Q-table for the first time
    return q_table

def load_q_table(file_path = 'q_table.pkl'):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_q_table(q_table, file_path = 'q_table.pkl'):
    with open(file_path, 'wb') as f:
        pickle.dump(q_table, f)

def choose_action(state, q_table, epsilon = 0.1):
    """Selects an action using epsilon-greedy policy."""
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(len(actions))
    else:
        return np.argmax(q_table[state])


def get_ir_reading_indices():
    """Select indices of the front and side IR sensors that are most relevant for maze navigation."""
    return [2, 3, 4, 5, 6]  # Adjust these indices based on your specific robot sensor configuration

def get_state_from_ir_values(ir_values, num_bins = 5, num_sensors = 5):
    """Bins IR sensor values and converts them into a single state index."""
    def bin_value(value):
        if value < 5:
            return 0  # No detection
        elif value < 10:
            return 1  # Detected far
        elif value < 15:
            return 2  # Detected mid-range
        elif value < 20:
            return 3  # Detected close
        else:
            return 4  # Very close or contact
    
    binned_values = [bin_value(value) for value in ir_values]
    state_index = 0
    for i, value in enumerate(binned_values):
        state_index += value * (num_bins ** i)
    
    return state_index

def simulate_robot_action(rob, action):
    """Simulates the robot's action and handles the consequences of that action."""
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
    selected_indices = get_ir_reading_indices()
    selected_values = [ir_values[idx] for idx in selected_indices]
    next_state = get_state_from_ir_values(selected_values)

    # Detect collisions
    if any(value < 20 for value in selected_values):
        reward = -50  # Penalty for potential collision
    else:
        reward = 1  # Reward for successful movement

    return next_state, reward

def train_q_table(rob, q_table, num_episodes = 200, max_steps = 100, alpha = 0.1, gamma = 0.9, epsilon = 0.1):
    """Trains the Q-table over a series of episodes."""
    for episode in range(num_episodes):
        if isinstance(rob, SimulationRobobo):
            rob.play_simulation()
            print("Start simulation: ", episode)

        ir_values = rob.read_irs()
        selected_indices = get_ir_reading_indices()
        selected_values = [ir_values[idx] for idx in selected_indices]
        state = get_state_from_ir_values(selected_values)

        done = False
        step = 0
        while not done:
            try:
                action_index = choose_action(state, q_table, epsilon)
                action = actions[action_index]
                next_state, reward = simulate_robot_action(rob, action)
                print("Next state:", next_state, "Reward:", reward)  # Debugging output

                best_next_action = np.argmax(q_table[next_state])
                q_table[state][action_index] += alpha * (reward + gamma * q_table[next_state][best_next_action] - q_table[state][action_index])
                
                state = next_state
                step += 1
                if reward == -50 or step >= max_steps:
                    done = True
                    if isinstance(rob, SimulationRobobo):
                        rob.stop_simulation()
            except Exception as e:
                print("An error occurred:", e)
                done = True
                if isinstance(rob, SimulationRobobo):
                    rob.stop_simulation()

    save_q_table(q_table)  # Save the trained Q-table

# Example of how you might set up the robot interface and start training
rob = SimulationRobobo()  # or HardwareRobobo() for actual hardware
q_table = initialize_q_table()
train_q_table(rob, q_table)