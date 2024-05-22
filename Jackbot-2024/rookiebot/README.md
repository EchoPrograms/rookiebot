# Team 3140 - Jackbot

Welcome to the repository for Flagship 3140's Jackbot code for the 2024 FRC season, themed "Crescendo". This README provides an overview of our robot, its subsystems, and how to use this codebase.

## References
- Unqualified Quokkas YouTube Channel
- WPILib GitHub repository:[ https://github.com/wpilibsuite/wpilib](url)
- WPILib documentation: [https://docs.wpilib.org/en/stable/docs/getting-started/programming-languages/python.html](url)
- WPILib Python API reference: [https://first.wpi.edu/wpilib/allwpilib/docs/py/index.html](url)
- WPILib Python sample projects:[ https://github.com/wpilibsuite/allwpilib/tree/master/wpilib/samples/Python](url)
- WPILib Python tutorials: https:[//docs.wpilib.org/en/stable/docs/tutorials/python.html](url)
- WPILib Python community forum: [https://www.chiefdelphi.com/forums/forumdisplay.php?f=158](url)
- WPILib Python Discord server: [https://discord.com/invite/Fp7KbkC](url)
- WPILib Python GitHub issues: [https://github.com/wpilibsuite/wpilib/issues](url)
- WPILib Python pull requests: [https://github.com/wpilibsuite/wpilib/pulls](url)
- WPILib Python development roadmap: [https://github.com/wpilibsuite/wpilib/projects/1](url)

## Actions
Our robot, Jackbot, is designed to:
- Pick up notes from the ground.
- Pick up notes from the human player station.
- Shoot notes in the speaker and amp.
- Drive under the stage.

It has the following subsystems:
- Arm
- Climber
- Shooter/Intake
- Drivetrain

### Teleop Strategy
During teleop, the player will control the robot to pick up notes on the ground on its side of the field and also go across the field to pick up notes dropped by the human player. The robot will then shoot the notes in both the speaker and the amp until the endgame buzzer goes off, and climb onto a chain (the stage), possibly climbing with another robot.

### Auto Strategy
To be determined.

## Subsystems

### Arm
The arm uses two motors to move up and down, which are configured as a group, allowing the intake/shooter subsystem to move to the ground to pick up the notes and move back up to shoot them.

| Component       | ID           | Interface       | Connection      | Role                                |
|-----------------|--------------|-----------------|-----------------|-------------------------------------|
| Arm Motor 1     | TalonSRX     | CAN ID:         |                 | A motor for controlling the arm    |
| Arm Motor 2     | TalonSRX     | CAN ID:         |                 | A motor for controlling the arm    |
| Arm Encoder     | TalonSRX     | CAN ID:         |                 | An absolute encoder for sensing the arm angle |

### Shooter/Intake
The intake and shooter are both in one subsystem, connected to the top of the arm and using one motor. It picks up a ground note using 2 sets of wheels, then another set of wheels pushes the note into a shooter where it is then shot into the air through another set of wheels.

| Component       | ID           | Interface       | Connection      | Role                                |
|-----------------|--------------|-----------------|-----------------|-------------------------------------|
| Intake Motor    | TalonSRX     | CAN ID:         |                 | A motor for controlling the intake |
| Shooter Motor 1 | TalonSRX     | CAN ID:         |                 | A motor for controlling the shooter|
| Shooter Motor 2 | TalonSRX     | CAN ID:         |                 | A motor for controlling the shooter|

### Climber
The climber is made up of two hooks that lift the robot off the ground in endgame.

| Component            | ID           | Interface       | Connection      | Role                                       |
|----------------------|--------------|-----------------|-----------------|--------------------------------------------|
| Climber Motor Left   | TalonSRX     | CAN ID: 14      |                 | A motor for controlling the left climber   |
| Climber Motor Right  | TalonSRX     | CAN ID: 15      |                 | A motor for controlling the right climber  |
| Solenoid Left        | Relay        | Relay Port: 0   |                 | A solenoid powered by a relay for the left climber  |
| Solenoid Right       | Relay        | Relay Port: 1   |                 | A solenoid powered by a relay for the right climber |

### Drivetrain
This robot uses tank drive to move, and it includes 4 Talon SRX motors, white/80A durometer HiGRip wheels, and an 8.46:1 gear ratio.

| Component               | ID           | Interface       | Connection      | Role                                |
|-------------------------|--------------|-----------------|-----------------|-------------------------------------|
| Turn Motor Front Left   | TalonSRX     | CAN ID:         |                 | A motor and encoder for driving left|
| Drive Motor Front Left  | TalonSRX     | CAN ID:         |                 | A motor and encoder for driving right|

## Getting Started
To deploy and run this code on the robot, follow these steps:

1. Open the project in your preferred IDE (we use WPIlib VSCode).
2. Ensure that all dependencies are correctly installed and configured.
3. Build the project to ensure there are no compilation errors.
4. Deploy the code to your robot using your preferred deployment method (we use Ethernet).
5. Test each subsystem to verify functionality.

## Contributing
If you would like to contribute to the robot code, please follow these guidelines:

- Do not code directly in the main branch, nor commit to main.
- Make your changes and ensure that the code compiles without errors.
- Test your changes thoroughly.
- Submit a pull request, describing the changes you've made and any relevant information.
