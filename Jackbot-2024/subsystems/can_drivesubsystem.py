"""
Copyright (c) Brogan 2024.
THIS IS MINE, U NO USEY
"""

from re import T
import commands2
import wpilib
import phoenix5
import math
import constants
from wpilib import drive

class DriveSubsystem(commands2.Subsystem):
    """
    This class represents the drivetrain subsystem of the robot.
    It initializes the motor controllers for the left and right sides of the drivetrain,
    and sets up a differential drive system.
    """
    def __init__(self, robotContainer) -> None:
        super().__init__()
        self.container = robotContainer

        # Initialize motor controllers for the left and right sides of the drivetrain
        self.left1 = phoenix5.WPI_TalonSRX(constants.kLeftMotor1Port)
        self.left2 = phoenix5.WPI_TalonSRX(constants.kLeftMotor2Port)
        self.right1 = phoenix5.WPI_TalonSRX(constants.kRightMotor1Port)
        self.right2 = phoenix5.WPI_TalonSRX(constants.kRightMotor2Port)

        # Set the right side motors to be inverted
        self.right1.setInverted(True)
        self.right2.setInverted(True)
        self.left1.setInverted(True)

        # Create motor controller groups for the left and right sides
        self.left = wpilib.MotorControllerGroup(self.left1, self.left2)
        self.right = wpilib.MotorControllerGroup(self.right1, self.right2)

        # Create a differential drive system
        self.tankDrive = wpilib.drive.DifferentialDrive(self.left, self.right)

        # Initialize the robot's starting position and rotation
        self.robotData = [0, 0, 0]
        self.robotData[0] = constants.kStartingX
        self.robotData[1] = constants.kStartingY
        self.robotData[2] = constants.kStartingRot

    def calculateDriving(self):
        """
        This method calculates the driving of the robot based on the driver's input.
        """
        forwardAxis = -self.container.driverController.getRawAxis(1) 
        turnAxis = -self.container.driverController.getRawAxis(4)

        # Only drive the robot if the forward or turn axis is not zero
        if(abs(forwardAxis) > 0.1 or abs(turnAxis) > 0.1):
            self.tankDrive.arcadeDrive(constants.kTankDriveSpeedMultiplier*forwardAxis, constants.kTankDriveSpeedMultiplier*turnAxis)

    def calculateSim(self):
        """
        This method calculates the robot's position and rotation for simulation.
        """
        leftPower = self.left1.get() + self.left2.get()
        rightPower = self.right1.get() + self.right2.get()
        fowardSpeed = (leftPower + rightPower) * constants.kSimulatedTimeConstant
        self.robotData[0] += math.cos(math.radians(self.robotData[2])) * fowardSpeed
        self.robotData[1] += math.sin(math.radians(self.robotData[2])) * fowardSpeed
        self.robotData[2] += (rightPower - leftPower) * constants.kSimulatedTurnRateConstant
        wpilib.SmartDashboard.putNumberArray("Field/Robot", self.robotData)

    def arcadeDrive(self, speed, turn):
        """
        This method drives the robot using arcade drive.
        """
        self.tankDrive.arcadeDrive(speed, turn)