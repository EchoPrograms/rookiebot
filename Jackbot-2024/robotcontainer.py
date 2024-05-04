#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button

import math
import constants

from commands.autos import Autos
from commands.launchnote import LaunchNote
from commands.preparelaunch import PrepareLaunch

from subsystems.can_drivesubsystem import DriveSubsystem
from subsystems.can_launchersubsystem import LauncherSubsystem
from subsystems.can_armsubsystem import ArmSubsystem



class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        self.driverController = commands2.button.CommandXboxController(
            constants.kDriverControllerPort
        )
        self.operatorController = commands2.button.CommandXboxController(
            constants.kOperatorControllerPort
        )

        

        # Simulation widgets

        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self.field)

        # measurements are from the cad sketch and are in inches
        self.armMechanism = wpilib.Mechanism2d(44, 44, wpilib.Color8Bit(wpilib.Color.kBlack))
        self.robotSegments = [self.armMechanism.getRoot("root", 2, 0)]
        # spacer to the robot bottom
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("chassisS", 12, 0, 0, wpilib.Color8Bit(0, 0, 0)))
        # bottom line
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("chassisB", 29, 0, 6, wpilib.Color8Bit(150, 150, 150)))
        
        # side lines
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-2].appendLigament("chassisS1", 3.5, 90, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-2].appendLigament("chassisS2", 3.5, 90, 6, wpilib.Color8Bit(150, 150, 150)))
        # top line
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-2].appendLigament("chassisT", 29, -90, 6, wpilib.Color8Bit(150, 150, 150)))
        # a frame spacers 
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-2].appendLigament("aFrameSpacerx", 1.25, 90, 0, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("aFrameSpacery", 2, 90, 0, wpilib.Color8Bit(150, 150, 150)))
        # a frame section
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("aFrame1", 7, 180+25.006645, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("aFrame2", 24.5, 80, 6, wpilib.Color8Bit(150, 150, 150)))
        # arm 
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-2].appendLigament("arm", 25.834702, 158.762371 - 180, 6, wpilib.Color8Bit(255, 255, 255)))
        self.armSegment = self.robotSegments[len(self.robotSegments)-1]
        # intake lines
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("intake1", 12.473505, 180 - 108.81, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("intake2", 5.339388, 94.735635 - 180, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("intake3", 15.996981, 94.846189 - 180, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("intake4", 8.011956, 85.209965 - 180, 6, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments.append(self.robotSegments[len(self.robotSegments)-1].appendLigament("intake5", 3.528768, 85.208210 - 180, 6, wpilib.Color8Bit(150, 150, 150)))
        
        wpilib.SmartDashboard.putData("Arm Mechanism", self.armMechanism)

        self.armMechanism3d = wpilib.Mechanism2d(1, 1, wpilib.Color8Bit(wpilib.Color.kBlack))
        self.robotSegments3d = [self.armMechanism3d.getRoot("root", 0.1, 0)]
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("armLocator", 0.226105, 61.781571, 0, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("arm", 0.660457, 180 - 155.550588, 3, wpilib.Color8Bit(255, 255, 255)))
        self.armSegment3d = self.robotSegments3d[len(self.robotSegments3d)-1]
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("intake1", 0.316827, 180 + 108.81, 5, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("intake2", 0.135620, 180 - 94.735635, 5, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("intake3", 0.406323, 180 - 94.846189, 5, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("intake4", 0.203504, 180 - 85.209965, 5, wpilib.Color8Bit(150, 150, 150)))
        self.robotSegments3d.append(self.robotSegments3d[len(self.robotSegments3d)-1].appendLigament("intake5", 0.089631, 180 - 85.208210, 5, wpilib.Color8Bit(150, 150, 150)))


        wpilib.SmartDashboard.putData("3dArm", self.armMechanism3d)

        # The robot's subsystems

        self.launcher = LauncherSubsystem()
        self.drive = DriveSubsystem(self)
        self.arm = ArmSubsystem(self)

        self.configureButtonBindings()

    def configureButtonBindings(self):
        self.operatorController.a().whileTrue(
            PrepareLaunch(self.launcher)
            .withTimeout(constants.kLauncherDelay)
            .andThen(LaunchNote(self.launcher))
            .handleInterrupt(lambda: self.launcher.stop())
        )

        self.operatorController.leftBumper().whileTrue(self.launcher.getIntakeCommand())

    def getAutonomousCommand(self) -> commands2.Command:
        return Autos.exampleAuto(self.drive)

    

        
