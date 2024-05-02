#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

#
# The constants module is a convenience place for teams to hold robot-wide
# numerical or boolean constants. Don't use this for any other purpose!
#

import math
import wpilib

# Operator Interface
kDriverControllerPort = 0
kOperatorControllerPort = 1

# Drivetrain
kLeftMotor1Port = 1
kLeftMotor2Port = 2
kRightMotor1Port = 3
kRightMotor2Port = 4

kDTCurrentLimit = 60

# Launcher
kFeederMotor = 5
kLauncherMotor = 6

kArmMotor1 = 7
kArmMotor2 = 8 

kLauncherSpeed = 1
kLaunchFeederSpeed = 1
kIntakeLauncherSpeed = -1
kIntakeFeederSpeed = -0.2
kLauncherDelay = 1

kTankDriveSpeedMultiplier = 0.75
kSimulatedTimeConstant = 0.02
kSimulatedTurnRateConstant = 3

kStartingX = 1.25
kStartingY = 7
kStartingRot = 180
