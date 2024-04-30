"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

from re import T
import commands2
import wpilib
import wpilib.drive
import rev
import phoenix5
import constants


class DriveSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()

        # Initialize motor controllers for the left and right sides of the drivetrain
        self.left1 = phoenix5.TalonFX(constants.kLeftMotor1Port)
        self.left2 = phoenix5.TalonFX(constants.kLeftMotor2Port)
        self.right1 = phoenix5.TalonFX(constants.kRightMotor1Port)
        self.right2 = phoenix5.TalonFX(constants.kRightMotor2Port)

        self.left1.setInverted(True)
        self.left2.setInverted(True)

       
    def calculateDriving(self):
        forwardAxis = self.driverController.getLeftY()
        turnAxis = self.driverController.getRightX()
        print(forwardAxis + ", " + turnAxis)
        
