# Import the necessary libraries
import navx
import wpilib
import wpilib.geometry

# TODO: Double-check the encoder channel assignments and ensure that they are correct
# TODO: Double-check the gyro connections and ensure that it is properly calibrated
# TODO: Make sure the encoders are equally spaced on either side of the robot and that the wheel diameters are identical
# TODO: Test the 'get_(measurement)' methods
# TODO: Test the reset_angle and reset_odometry methods to ensure they properly reset the angle and odometry.
# TODO: Ensure that the periodic method is called periodically in the main robot loop to update the odometry.

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
    
    def get_distance_driven(self):

        # Calculate the distance driven by the robot
        left_distance = self.left_encoder.getDistance() 
        right_distance = self.right_encoder.getDistance()

        distance = (left_distance + right_distance) / 2.0

        return distance

    def get_heading(self):

        #Get the current heading of the robot
        return self.get_angle() % 360.0

    def get_pose(self):

        # Get the current pose of the robot
        return self.odometry.getPoseMeters()

    def get_velocity(self):

        # Calculate the velocity of the robot
        left_velocity = self.left_encoder.getRate() 
        right_velocity = self.right_encoder.getRate()

        velocity = (left_velocity + right_velocity) / 2.0

        return velocity

    def get_yaw_rate(self):

        # Get the current yaw rate of the robot
        return self.ahrs.getRate()

    def get_rotation_matrix(self):

        # Get the rotation matrix of the robot
        angle = self.get_angle()

        rotation_matrix = wpilib.geometry.Rotation2d(wpilib.math.angle.Degrees(angle))

        return rotation_matrix

    def get_translation_vector(self):

        # Get the translation vector of the robot
        pose = self.get_pose()

        translation_vector = pose.getTranslation()

        return translation_vector

    def get_rotation_vector(self):

        # Get the rotation vector of the robot
        pose = self.get_pose()

        rotation_vector = pose.getRotation()

        return rotation_vector

    def get_distance_driven_in_inches(self):

        # Calculate the distance driven by the robot in inches
        distance = self.get_distance_driven()

        distance_in_inches = distance * 25.4

        return distance_in_inches

    def get_distance_driven_in_feet(self):

        # Calculate the distance driven by the robot in feet
     distance = self.get_distance_driven()

     distance_in_feet = distance / 12.0

     return distance_in_feet
