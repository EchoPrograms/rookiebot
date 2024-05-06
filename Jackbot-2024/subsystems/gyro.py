# Import the necessary libraries
import navx
import wpilib
import wpilib.geometry

class Gyro:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize the navx here
        self.ahrs = navx.AHRS.create_spi()

        # Initialize the odometry here
        self.left_encoder = wpilib.drive.Encoder(0, 1, False, wpilib.drive.Encoder.EncodingType.k4X)
        self.right_encoder = wpilib.drive.Encoder(2, 3, False, wpilib.drive.Encoder.EncodingType.k4X)

        # Set the starting position of the robot
        self.start_pose = wpilib.geometry.Pose2d(0, 0, self.get_angle())

        # Initialize the odometry with the starting position and the navx angle
        self.odometry = wpilib.geometry.Odometry(self.start_pose, self.get_angle(), self.left_encoder, self.right_encoder)

    def get_angle(self):
        # Get the current angle from the navx
        return self.ahrs.getAngle()

    def get_relative_pose2d(self):
        # Get the location of the robot relative to the starting point
        return self.odometry.getPoseMeters()

    def reset_angle(self):
        # Reset the angle to zero
        self.ahrs.reset()
        self.odometry.resetPosition(self.start_pose, self.get_angle())

    def periodic(self):
        # Update the odometry
        # This method is called periodically to update the odometry
        self.odometry.update(self.get_angle(), self.left_encoder.getDistance(), self.right_encoder.getDistance())

    def reset_odometry(self):
        # Reset the odometry to the starting position and angle
        self.odometry.resetPosition(self.start_pose, self.get_angle())