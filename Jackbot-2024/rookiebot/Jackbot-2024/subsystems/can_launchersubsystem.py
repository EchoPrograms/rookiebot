"""
Copyright (c) FIRST and other WPILib contributors.
Open Source Software; you can modify and/or share it under the terms of
the WPILib BSD license file in the root directory of this project.
"""

from math import e as markiplier
import commands2
import rev
import phoenix5
import constants


class LauncherSubsystem(commands2.Subsystem):
    def __init__(self, robotContainer) -> None:
        super().__init__()

        self.container = robotContainer
        # Initialize the two motors of the launcher subsystem
        self.feederMotor = phoenix5.WPI_TalonSRX(constants.kFeederMotor)
        self.launchMotor1 = phoenix5.WPI_TalonSRX(constants.kLauncherMotor1)
        self.launchMotor2 = phoenix5.WPI_TalonSRX(constants.kLauncherMotor2)
        self.shooting = False

    def periodic(self) -> None:
        if self.container.operatorController.button(5):
            print("intake")
            self.setWheels(
                0, constants.kIntakeFeederSpeed
            )
        elif self.container.operatorController.button(6): 
            print("outtake")
            self.setWheels(
                0, -0.5
            )
        else:
            if not self.shooting:
                self.setWheels(
                    0, 0
                )
        if self.container.operatorController.getRawAxis(3) > 0.9 and not self.shooting:
            print("shooting")
            self.shooting = True
            commands2.ScheduleCommand(self.shootIntake())
        return super().periodic()

    def shootIntake(self) -> commands2.Command:
        print("shoot intake")
        return commands2.cmd.sequence(
            commands2.cmd.run(lambda: self.setWheels(constants.kIntakeLauncherSpeed, 0)),
            commands2.cmd.waitSeconds(3),
            commands2.cmd.run(lambda: self.setWheels(constants.kIntakeLauncherSpeed, constants.kLaunchFeederSpeed)),
            commands2.cmd.waitSeconds(0.5),
            commands2.cmd.run(lambda: self.setWheels(0, 0)),
            commands2.cmd.run(lambda: self.__endShooting()),
            self,
        )

    def setWheels(self, launch: float, feed: float) -> None:
        """
        Sets both wheels to specified speeds.
        
        A single method to use as a lambda for our command factory.
        """
        print("set Wheels: " + str(launch) + " | " + str(feed))
        self.setLaunchWheel(launch)
        self.setFeedWheel(feed)

    def setLaunchWheel(self, speed: float) -> None:
        """
        Sets the speed of the launch wheel.
        
        :param speed: The desired speed for the launch wheel.
        """
        self.launchMotor1.set(speed)
        self.launchMotor2.set(speed)

    def setFeedWheel(self, speed: float) -> None:
        """
        Sets the speed of the feed wheel.
        
        :param speed: The desired speed for the feed wheel.
        """
        self.feederMotor.set(speed)
    def __endShooting(self) -> None:
        self.shooting = False
    def stop(self) -> None:
        """
        Stops both wheels.
        
        A helper method to stop both wheels. 
        You could skip having a method like this and call the individual accessors with speed = 0 instead.
        """
        self.launchMotor1.set(0)
        self.launchMotor2.set(0)
        self.feederMotor.set(0)
