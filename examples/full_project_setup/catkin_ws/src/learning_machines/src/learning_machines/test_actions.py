import cv2

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


def test_emotions(rob: IRobobo):
    rob.set_emotion(Emotion.HAPPY)
    rob.talk("Hello")
    rob.play_emotion_sound(SoundEmotion.PURR)
    rob.set_led(LedId.FRONTCENTER, LedColor.GREEN)


def test_move_and_wheel_reset(rob: IRobobo):
    rob.move_blocking(100, 100, 1000)  # the 1st 100 is the speed for the left wheel, while the second 100 is the speed for the right wheel. The 3rd argument (1000) is the duaration of the action (movement) in milliseconds. The method 'move_blocking' is used to ensure that the robot completes this movement before proceeding to the next line of code, effectively "blocking" further execution until the movement is complete.
    print("before reset: ", rob.read_wheels()) # return the encoder values from the robot's wheels. These values indicate how much the wheels have rotated, which can be used to estimate distance traveled, among other things.
    rob.reset_wheels() # resetting wheel encoders to zero is commonly done to clear any previous movement data, ensuring that future readings start from a known state of zero. 
    rob.sleep(1) # this pauses the execution of the function for 1 second. This delay is often used to provide time buffers between the actions.
    print("after reset: ", rob.read_wheels()) # prints the wheel encoder values again after the reset operation. This should ideally show zeros or values very close to zero, confirming that the reset was successful.


def test_sensors(rob: IRobobo):
    print("IRS data: ", rob.read_irs()) # prints the data from the robot's infrared sensors (IRS).
    image = rob.get_image_front() # an image is captured from the robot's front-facing camera.
    cv2.imwrite(str(FIGRURES_DIR / "photo.png"), image) # saves the captured image to a file.
    print("Phone pan: ", rob.read_phone_pan()) # pan: horizontal rotation
    print("Phone tilt: ", rob.read_phone_tilt()) # tilt: the precise angle at which the phone is set, which can affect camera view, sensor reading, etc.
    print("Current acceleration: ", rob.read_accel())
    print("Current orientation: ", rob.read_orientation())


def test_phone_movement(rob: IRobobo):
    rob.set_phone_pan_blocking(20, 100) # commands the robot to adjust the pan (horizontal orientation) of the phone to 20 degrees. 100 is the duration of the movement or the speed (optional parameter).
    print("Phone pan after move to 20: ", rob.read_phone_pan()) # prints the current pan position to verify that the phone has indeed moved to the desired angle.
    rob.set_phone_tilt_blocking(50, 100) # adjusts the tilt (vertical orientation) of the phone to 50 degrees, with execution blocking until the movement is completed.
    print("Phone tilt after move to 50: ", rob.read_phone_tilt()) # prints the current tilt position of the phone after the adjustment. This confirms that the tilt angle has been set as intended.


def test_sim(rob: SimulationRobobo):
    print(rob.get_sim_time()) # prints the current simulation time, which represents how much virtual time has elapsed since the simulation started.
    print(rob.is_running()) # checks and prints whether the simulation is currently active (running). Boolean value.
    rob.stop_simulation() # stops the simulation.
    print(rob.get_sim_time()) # prints the simulation time. This is to confirm that the 'stop_simulation()' command was effective.
    print(rob.is_running()) # prints the running state. This is to confirm that the 'stop_simulation()' command was effective.
    rob.play_simulation() # restarts the simulation.
    print(rob.get_sim_time()) # prints the updated simulation time to show any progression in virtual time.
    print(rob.get_position()) # prints the robot's current position within the simulation environment.


def test_hardware(rob: HardwareRobobo):
    print("Phone battery level: ", rob.read_phone_battery())
    print("Robot battery level: ", rob.read_robot_battery())


def run_all_actions(rob: IRobobo):
    if isinstance(rob, SimulationRobobo):
        rob.play_simulation()
    test_emotions(rob)
    test_sensors(rob)
    test_move_and_wheel_reset(rob)
    if isinstance(rob, SimulationRobobo):
        test_sim(rob)

    if isinstance(rob, HardwareRobobo):
        test_hardware(rob)

    test_phone_movement(rob)

    if isinstance(rob, SimulationRobobo):
        rob.stop_simulation()


# Our initial concept/scene for Task 0
def move_robot(rob: IRobobo):
    """Moves the robot straight until an object is detected, then turns right."""
    if isinstance(rob, SimulationRobobo): 
        rob.play_simulation()

    ir_values = rob.read_irs()

    # IR sensors detect an object
    if all(value < 20 for value in ir_values[2:6]):  # threshold value 
        # Stop moving forward
        rob.move(0, 0, 0)
        rob.sleep(0.5)

        # Turn right
        rob.move(50, -50, 1000) 
        #rob.block()

    else:
        # Move forward
        rob.move(50, 50, 1000)
        #rob.block()
    
    rob.sleep(0.1)

        #if isinstance(rob, SimulationRobobo):
            #rob.stop_simulation()


# Our final concept/scene for Task 0
def avoid_object(rob: IRobobo):
    """
    This function directs the robot to move straight until it detects an object nearby.
    Upon detection, the robot will change its emotion to indicate awareness or caution,
    then turn left to avoid the object.
    """
    if isinstance(rob, SimulationRobobo): 
        rob.play_simulation()

    objects_detected = 0
    ir_values_list = []  # List to store IR sensor values

    while True:
        ir_values = rob.read_irs()
        print("ir value: ", ir_values[4])
        ir_values_list.append(ir_values[4])

        # Check if any of the front sensors detect an object within a close range
        # if any(value > 15 for value in ir_values[2:4]):  # threshold value as needed
        if ir_values[4] > 30 and ir_values[4] < 1500:
            rob.set_emotion(Emotion.SURPRISED)  # change the robot's emotion
            rob.talk("Oh object detected!")  # have the robot acknowledge the detection
            objects_detected += 1
            
            # Stop moving forward
            rob.move(0, 0, 0)
            rob.sleep(0.5)
            
            # Turn left
            rob.move(-50, 50, 800)  # speed values
            rob.sleep(1)
            
            if objects_detected == 2: 
                rob.talk(f"I detected {objects_detected} objects!")
                break  # Ecdxit the loop if you only want to avoid one obstacle, or continue if scanning for more

        else:
            # Continue moving forward
            rob.move(50, 50, 1000)

    rob.sleep(1)

    if isinstance(rob, SimulationRobobo):
        rob.stop_simulation()


    