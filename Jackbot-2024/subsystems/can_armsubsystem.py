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
    def __init__(self, robotContainer) -> None:
        super().__init__()
        self.container = robotContainer
        self.encoder = wpilib.DutyCycleEncoder(constants.kArmEncoderPort)
        self.left = phoenix5.WPI_TalonSRX(constants.kArmMotor1)
        self.right = phoenix5.WPI_TalonSRX(constants.kArmMotor2)

        self.armMotors = wpilib.MotorControllerGroup(self.left, self.right)

        self.right.setInverted(True)
    
    def periodic(self) -> None:
        armValue = -self.container.driverController.getRawAxis(5) 
        encoderAngle = self.getEncoderDegrees()
        if abs(armValue) > 0.1:
            self.container.armSegment.setAngle(self.container.armSegment.getAngle() + armValue * constants.kArmSpeedModifier * 4)
            self.container.armSegment3d.setAngle(self.container.armSegment.getAngle() + armValue * constants.kArmSpeedModifier * 4)
        if abs(armValue) > 0.1 and (encoderAngle < 330 or armValue < 0) and (encoderAngle > 240 or armValue > 0):
            self.armMotors.set(armValue * constants.kArmSpeedModifier  - constants.kMomentOfInertia * math.cos(math.radians(-(encoderAngle - 330))))
            
        else:
            self.armMotors.set(0 - constants.kMomentOfInertia * math.cos(math.radians(-(encoderAngle - 330))))
        wpilib.SmartDashboard.putNumber("Arm/d_armEndoder", encoderAngle)
        return super().periodic()
    def getEncoderDegrees(self) -> float:
        return self.encoder.getAbsolutePosition() * 360 





    


        
        
