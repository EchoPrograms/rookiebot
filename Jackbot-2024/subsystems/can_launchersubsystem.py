"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

import commands2
import rev
import phoenix5
import constants


class LauncherSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        # Initialize the two motors of the launcher subsystem
        self.feedWheel = phoenix5.WPI_TalonFX(constants.kFeederMotor)
        self.launchWheel = phoenix5.WPI_TalonFX(constants.kLauncherMotor)


    def getIntakeCommand(self) -> commands2.Command:
        """
        Returns a command to intake balls.
        
        The startEnd helper method takes a method to call when the command is initialized
        and one to call when it ends.
        """
        return commands2.cmd.startEnd(
            # When the command is initialized, set the wheels to the intake speed values
            lambda: self.setWheels(
                constants.kIntakeLauncherSpeed, constants.kIntakeFeederSpeed
            ),
            # When the command stops, stop the wheels
            lambda: self.stop(),
            self,
        )

    def setWheels(self, launch: float, feed: float) -> None:
        """
        Sets both wheels to specified speeds.
        
        A single method to use as a lambda for our command factory.
        """
        self.setLaunchWheel(launch)
        self.setFeedWheel(feed)

    def setLaunchWheel(self, speed: float) -> None:
        """
        Sets the speed of the launch wheel.
        
        :param speed: The desired speed for the launch wheel.
        """
        self.launchWheel.set(speed)

    def setFeedWheel(self, speed: float) -> None:
        """
        Sets the speed of the feed wheel.
        
        :param speed: The desired speed for the feed wheel.
        """
        self.feedWheel.set(speed)

    def stop(self) -> None:
        """
        Stops both wheels.
        
        A helper method to stop both wheels. 
        You could skip having a method like this and call the individual accessors with speed = 0 instead.
        """
        self.launchWheel.set(0)
        self.feedWheel.set(0)
