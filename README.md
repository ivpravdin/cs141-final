 # Autonomous payload lifting with COEX Clover 4


## Files:
- README.md: this file
- payload_lift.py: autonomous flight file

## Running 
First connect to COEX Clover 4 via SSH. Ensure that drone is in working condition by running

    rosrun clover selfcheck.py

If self-check fails, do **NOT** execute any files. Make sure that correct ArUco map is attached to the floor. Modify the algorithm as needed. Take caution while working with a drone.

To run the autonomous flight file, execute
    
    ./python3 payload_lift.py
