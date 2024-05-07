# DifferentialDrive.py

import wpilib
import wpilib.drive
import commands2
from rev import CANSparkMax
import phoenix5
import time

import constants
import gyro


# TODO: Add odom calculations
# TODO: Update motor controller types

class TalonMotorController(wpilib.interfaces.MotorController):
    def __init__(self, talon: phoenix5.TalonSRX, *args):
        super().__init__(*args)
        self.is_enabled = True
        self.talon = talon

    def set(self, speed: float) -> None:
        if self.is_enabled:
            self.talon.set(phoenix5.ControlMode.PercentOutput, speed)
        else:
            self.talon.set(phoenix5.ControlMode.PercentOutput, 0)

    def get(self) -> float:
        return self.talon.get()

    def setInverted(self, isInverted: bool) -> None:
        self.talon.setInverted(isInverted)

    def getInverted(self) -> bool:
        return self.talon.getInverted()

    def disable(self) -> None:
        self.is_enabled = False
        self.set(0)

    def enable(self) -> None:
        self.is_enabled = True

    def stopMotor(self) -> None:
        self.set(0)


class DifferentialDrive(commands2.Subsystem):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()
        
        # Initialize gyro
        self.gyro = gyro.Gyro.get_instance()

        self.frame_id = 0

        # Motor CAN IDs
        self.kLeftSparkCANId = 9
        self.kLeftTalon1CANId = 4
        self.kLeftTalon2CANId = 6

        self.kRightSparkCANId = 8
        self.kRightTalon1CANId = 5
        self.kRightTalon2CANId = 7

        self.kCurrentLimit = 40

        # Initialize motors
        self.left_motor1 = CANSparkMax(self.kLeftSparkCANId, CANSparkMax.MotorType.kBrushless)
        self.left_talon2 = phoenix5.TalonSRX(self.kLeftTalon1CANId)
        self.left_talon3 = phoenix5.TalonSRX(self.kLeftTalon2CANId)

        self.right_motor1 = CANSparkMax(self.kRightSparkCANId, CANSparkMax.MotorType.kBrushless)
        self.right_talon2 = phoenix5.TalonSRX(self.kRightTalon1CANId)
        self.right_talon3 = phoenix5.TalonSRX(self.kRightTalon2CANId)

        # Initialize Talon Motor Controllers
        self.left_motor2 = TalonMotorController(self.left_talon2)
        self.left_motor3 = TalonMotorController(self.left_talon3)

        self.right_motor2 = TalonMotorController(self.right_talon2)
        self.right_motor3 = TalonMotorController(self.right_talon3)

        # Set motors to brake when not receiving signal
        self.left_motor1.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.right_motor1.setIdleMode(CANSparkMax.IdleMode.kBrake)

        # Set current limit on motors
        self.left_motor1.setSmartCurrentLimit(self.kCurrentLimit)
        self.right_motor1.setSmartCurrentLimit(self.kCurrentLimit)

        # Set motors to reverse so that positive voltages move the robot forward
        self.left_motor1.setInverted(True)
        self.left_motor2.setInverted(False)
        self.left_motor3.setInverted(False)

        self.right_motor1.setInverted(False)
        self.right_motor2.setInverted(True)
        self.right_motor3.setInverted(True)

        # Get spark max encoders
        self.leftEncoder = self.left_motor1.getEncoder()
        self.rightEncoder = self.right_motor1.getEncoder()

        # Group motors
        self.leftMotors = wpilib.MotorControllerGroup(
            self.left_motor1,
            self.left_motor2,
            self.left_motor3
        )

        self.rightMotors = wpilib.MotorControllerGroup(
            self.right_motor1,
            self.right_motor2,
            self.right_motor3
        )

        # Initialize drive
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

    def periodic(self, timestamp: float) -> None:
        """
        Periodic function called every 20ms.

        :param timestamp: the current timestamp
        """
        self.frame_id += 1
        if self.frame_id % 50 == 0:
            print("System Time:", timestamp)
            print("Left Encoder: ", self.leftEncoder.getPosition())
            print("Right Encoder: ", self.rightEncoder.getPosition())
            print("done")

    def arcadeDrive(self, fwd: float, rot: float, gyro: gyro.Gyro) -> None:
        # Calculate the rotational input based on the robot's heading
        rotational_input = rot - gyro.get_heading()

        # Limit the rotational input to a reasonable range
        rotational_input = max(-1.0, min(1.0, rotational_input))

        # Drive the robot using arcade controls with the updated rotational input
        self.drive.arcadeDrive(fwd, rotational_input)

    def stop(self) -> None:
        """
        Stops the drive from moving.
        """
        self.arcadeDrive(0, 0)

    def resetEncoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""
        self.leftEncoder.reset()
        self.rightEncoder.reset()

    def getAverageEncoderDistance(self) -> float:
        """
        Gets the average distance of the two encoders.

        :returns: the average of the two encoder readings
        """
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2.0

    def getLeftEncoder(self) -> wpilib.Encoder:
        """
        Gets the left drive encoder.

        :returns: the left drive encoder
        """
        return self.leftEncoder

    def getRightEncoder(self) -> wpilib.Encoder:
        """
        Gets the right drive encoder.

        :returns: the right drive encoder
        """
        return self.rightEncoder

    def setMaxOutput(self, maxOutput: float) -> None:
        """
        Sets the max output of the drive. Useful for scaling the drive to drive more slowly.

        :param maxOutput: the maximum output to which the drive will be constrained
        """
        self.drive.setMaxOutput(maxOutput)
