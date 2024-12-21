 # Autonomous Payload Lifting with COEX Clover 4


## Files:
- README.md: this file
- payload_lift.py: autonomous flight file

## Setup:
Instructions for physically assembling the drone and updating firmware can be found within the [documentation](https://clover.coex.tech/en/) for the COEX Clover drone, which includes Raspberry Pi image with a pre-configured Wi-Fi access point named `clover-xxxx`. This image and other additional resources are available on [GitHub](https://github.com/CopterExpress/clover).

## Running
_As a side note, ensure the drone's LiPo battery is fully charged before running._

First, connect your computer to the drone's `clover-xxxx` Wi-Fi network with the password `cloverwifi` ("xxxx" is a placeholder for the drone's numeric identifier). Then, connect to the drone via SSH by running the command

    ssh pi@192.168.11.1

The password to connect is set as `raspberry` upon fresh installation of the provided Pi image.

Once the connection has been established, ensure that drone is in working condition by running

    rosrun clover selfcheck.py

If self-check fails, do **NOT** execute any files. Make sure that correct ArUco map is attached to the floor. Modify the algorithm as needed. Take caution while working with a drone.

To run the autonomous flight file, execute
    
    python3 payload_lift.py
