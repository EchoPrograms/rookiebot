#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import constants
from subsystems.can_launchersubsystem import LauncherSubsystem

class LaunchNote(commands2.Command):

    def __init__(self, launcher: LauncherSubsystem) -> None:
        super().__init__()
        self.launcher = launcher
        self.addRequirements(launcher)

    def initialize(self) -> None:
        self.launcher.setWheels(constants.kLauncherSpeed, constants.kIntakeFeederSpeed)
        print("LAUUNCHHINGG")

    def isFinished(self) -> bool:
        return True
