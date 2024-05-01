#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
import constants
from wpilib.simulation import DifferentialDrivetrainSim
from wpimath.system.plant import DCMotor
from wpimath.system.plant import LinearSystemId


class TalonFXMotorSim:
    def __init__(self, motor, kvVoltSecondsPerMeter, kDistancePerPulse) -> None:
        self.simCollection = motor.getSimCollection()
        self.kvVoltSecondsPerMeter = kvVoltSecondsPerMeter
        self.kDistancePerPulse = kDistancePerPulse

    def update(self, dt) -> None:
        voltage = self.simCollection.getMotorOutputLeadVoltage()
        velocity = voltage / self.kvVoltSecondsPerMeter

        self.simCollection.setIntegratedSensorVelocity(
            int(velocity / self.kDistancePerPulse / 10)
        )
        self.simCollection.addIntegratedSensorPosition(
            int(velocity * dt / self.kDistancePerPulse)
        )

    def getVoltage(self):
        return self.simCollection.getMotorOutputLeadVoltage()

class PhysicsEngine:
    def __init__(self, physics_controller, robot):

        self.physics_controller = physics_controller

        self.left1 = TalonFXMotorSim(
            robot.container.drive.left1,
            constants.kvVoltSecondsPerMeter,
            constants.kDrivetrainEncoderDistancePerPulse)
        self.left2 = TalonFXMotorSim(
            robot.container.drive.left2,
            constants.kvVoltSecondsPerMeter,
            constants.kDrivetrainEncoderDistancePerPulse)
        self.right1 = TalonFXMotorSim(
            robot.container.drive.right1,
            constants.kvVoltSecondsPerMeter,
            constants.kDrivetrainEncoderDistancePerPulse)
        self.right2 = TalonFXMotorSim(
            robot.container.drive.right2,
            constants.kvVoltSecondsPerMeter,
            constants.kDrivetrainEncoderDistancePerPulse)

        self.system = LinearSystemId.identifyDrivetrainSystem(
            constants.kvVoltSecondsPerMeter,
            constants.kaVoltSecondsSquaredPerMeter,
            2.5,  # The angular velocity gain, in volt seconds per angle.
            0.3,  # The angular acceleration gain, in volt seconds^2 per angle.
        )
        self.drivesim = DifferentialDrivetrainSim(
            self.system,
            constants.kTrackWidthMeters,
            DCMotor.falcon500(constants.kDrivetrainMotorCount),
            constants.kDrivetrainGearRatio,
            (constants.kDrivetrainWheelDiameterMeters / 2),
        )


    def update_sim(self, now, tm_diff):
        self.left1.update(tm_diff)
        self.left2.update(tm_diff)
        self.right1.update(tm_diff)
        self.right2.update(tm_diff)

        self.drivesim.setInputs(-self.left1.getVoltage(),
                                self.right1.getVoltage())
        self.drivesim.update(tm_diff)
