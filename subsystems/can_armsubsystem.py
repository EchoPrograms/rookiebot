"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

from json import encoder
from tokenize import Double
import commands2
import wpilib
import phoenix5
import constants
import math

class ArmSubsystem(commands2.Subsystem):
    """
    A class representing the arm subsystem of a robot.
    """

    def __init__(self, robotContainer) -> None:
        """
        Initialize the arm subsystem.

        :param robotContainer: The robot container object.
        """
        super().__init__()
        self.container = robotContainer  # Set the robot container
        self.encoder = wpilib.DutyCycleEncoder(constants.kArmEncoderPort)  # Initialize the arm encoder
        self.left = phoenix5.WPI_TalonSRX(constants.kArmMotor1)  # Initialize the left arm motor
        self.right = phoenix5.WPI_TalonSRX(constants.kArmMotor2)  # Initialize the right arm motor

        self.armMotors = wpilib.MotorControllerGroup(self.left, self.right)  # Create a motor controller group for the arm motors

        self.right.setInverted(True)  # Set the right arm motor to be inverted

    def periodic(self) -> None:
        """
        The periodic method of the arm subsystem.
        This method is called by the robot scheduler at regular intervals.
        """
        armValue = -self.container.driverController.getRawAxis(5)  # Get the value of the arm joystick
        encoderAngle = self.getEncoderDegrees()  # Get the current angle of the arm encoder
        if abs(armValue) > 0.1:  # If the arm joystick value is greater than 0.1
            self.container.armSegment3d.setAngle(max(min(self.container.armSegment3d.getAngle() + armValue * constants.kArmSpeedModifier * 4, 33.119908), -51.402775))  # Set the angle of the arm segment
        if abs(armValue) > 0.1 and (encoderAngle < 330 or armValue < 0) and (encoderAngle > 240 or armValue > 0):  # If the arm joystick value is greater than 0.1 and the arm encoder angle is within a certain range
            self.armMotors.set(armValue * constants.kArmSpeedModifier  - constants.kMomentOfInertia * math.cos(math.radians(-(encoderAngle - 330))))  # Set the speed of the arm motors
        else:
            self.armMotors.set(0 - constants.kMomentOfInertia * math.cos(math.radians(-(encoderAngle - 330))))  # Set the speed of the arm motors to 0
        wpilib.SmartDashboard.putNumber("Arm/d_armEndoder", encoderAngle)  # Put the arm encoder angle on the SmartDashboard
        return super().periodic()

    def getEncoderDegrees(self) -> float:
        """
        Get the current angle of the arm encoder in degrees.

        :return: The current angle of the arm encoder in degrees.
        """
        return self.encoder.getAbsolutePosition() * 360  # Return the current angle of the arm encoder in degree