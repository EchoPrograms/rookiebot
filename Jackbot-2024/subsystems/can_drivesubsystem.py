"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

from re import T
import commands2
import wpilib
import phoenix5
import math
import constants
from wpilib import drive


class DriveSubsystem(commands2.Subsystem):
    def __init__(self, robotContainer) -> None:
        super().__init__()
        self.container = robotContainer

        self.robotData = [0, 0, 0]
        # Initialize motor controllers for the left and right sides of the drivetrain
        self.left1 = phoenix5.WPI_TalonFX(constants.kLeftMotor1Port)
        self.left2 = phoenix5.WPI_TalonFX(constants.kLeftMotor2Port)
        self.right1 = phoenix5.WPI_TalonFX(constants.kRightMotor1Port)
        self.right2 = phoenix5.WPI_TalonFX(constants.kRightMotor2Port)


        self.right1.setInverted(True)
        self.right2.setInverted(True)
        
        self.left = wpilib.MotorControllerGroup(self.left1, self.left2)
        self.right = wpilib.MotorControllerGroup(self.right1, self.right2)
        self.tankDrive = wpilib.drive.DifferentialDrive(self.left, self.right)

        

       
    def calculateDriving(self):
        forwardAxis = -self.container.driverController.getRawAxis(1)
        turnAxis = -self.container.driverController.getRawAxis(4)
        
        if(abs(forwardAxis) > 0.1 or abs(turnAxis) > 0.1):
            self.tankDrive.arcadeDrive(constants.kTankDriveSpeedMultiplier*forwardAxis, constants.kTankDriveSpeedMultiplier*turnAxis)

    def calculateSim(self):
        leftPower = self.left1.get() + self.left2.get()
        rightPower = self.right1.get() + self.right2.get()
        fowardSpeed = (leftPower + rightPower) * constants.kSimulatedTimeConstant * ((self.container.driverController.getRawAxis(3) * 2) + 1)
        self.robotData[0] += math.cos(math.radians(self.robotData[2])) * fowardSpeed
        self.robotData[1] += math.sin(math.radians(self.robotData[2])) * fowardSpeed
        self.robotData[2] += (rightPower - leftPower) * constants.kSimulatedTurnRateConstant
        wpilib.SmartDashboard.putNumberArray("Field/Robot", self.robotData)

        

        
        
