#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import constants

# from subsystems.can_drivesubsystem import DriveSubsystem
from subsystems.can_drivesubsystem import DriveSubsystem


class Autos(commands2.Command):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        self.drive = drive
        self.addRequirements(drive)

    def exampleAuto(self) -> commands2.Command:
        return (
            commands2.cmd.run(lambda: self.drive.arcadeDrive(-0.5, 0), self.drive)
            .withTimeout(1.0)
            .andThen(
                commands2.cmd.run(lambda: self.drive.arcadeDrive(0, 0), self.drive)
            )
        )
