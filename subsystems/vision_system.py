# TODO: If we want to use the vision system's output to control the robot's movements or actions, we have to modify the commands2 files (e.g., AutonomousCommand.py, TeleopCommand.py) to access the vision system's data and make decisions based on it.
# TODO: If we want to display the vision system's output on the dashboard, we need to modify the dashboard files (e.g., Dashboard.py) to include widgets that display the vision system's data.
# TODO: Call the process_images method in the robotPeriodic method
# TODO: Camera calibration 
# TODO: Add error handling
# TODO: Test and debug
# TODO: Create a Number Display widget in Drivers station so that we can access the vision processing output

import cv2
from photonvision import PhotonCamera
from wpilib import SmartDashboard

class VisionSystem:
    def __init__(self):
        self.cam = PhotonCamera()

    def process_images(self):
        # Capture an image from the camera
        ret, frame = self.cam.capture()

        # Process the image using PhotonVision
        result = self.cam.getLatestResult()

        # If a target is detected, print the angle and distance
        if result is not None:
            print(f"Target detected at angle {result.target.angle} and distance {result.target.distance}")

            # Send the angle and distance to the SmartDashboard
            SmartDashboard.putNumber("Target Angle", result.target.angle)
            SmartDashboard.putNumber("Target Distance", result.target.distance)

        else:
            # If no target is detected, send a default value to the SmartDashboard
            SmartDashboard.putNumber("Target Angle", 0.0)
            SmartDashboard.putNumber("Target Distance", 0.0)

        # Display the output
        cv2.imshow('frame', frame)

        # Exit on key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cam.release()
            cv2.destroyAllWindows()
            exit()

    def shutdown(self):
        self.cam.release()
        cv2.destroyAllWindows()
