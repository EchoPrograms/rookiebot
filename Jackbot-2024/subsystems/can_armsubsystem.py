"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

import commands2
import wpilib
import phoenix5
import constants



class ArmSubsystem(commands2.Subsystem):
    def __init__(self, robotContainer) -> None:
        super().__init__()
        self.container = robotContainer
        self.encoder = wpilib.Encoder(constants.kArmMotor1, constants.kArmMotor2)
        self.left = phoenix5.WPI_TalonFX(constants.kArmMotor1)
        self.right = phoenix5.WPI_TalonFX(constants.kArmMotor2)

        self.right.setInverted(True)


        
        
