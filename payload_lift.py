import rospy
import math
import sys
from clover import srv
from std_srvs.srv import Trigger
from aruco_pose.msg import MarkerArray

# Initialize the node
rospy.init_node('flight') 

# Service proxies
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
set_yaw_rate = rospy.ServiceProxy('set_yaw_rate', srv.SetYawRate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

# Navigate and wait (Algorithm 1)
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        # print(telem.x ** 2 + telem.y ** 2 + telem.z ** 2)
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

# Take off
navigate_wait(x=0, y=0, z=0.4, speed=0.1, frame_id='body', auto_arm=True)
print("Move 0 complete")

marker_detected = False
global aruco_detect 

def markers_callback(msg):
    global marker_detected
    for marker in msg.markers:
        if marker.id == 119:
            tel_119 = get_telemetry(frame_id='aruco_119')
            print(tel_119)
            
            marker_detected = True
            print('Aruco 119 detected')
            aruco_detect.unregister()
            break

# Subscribe to the aruco_detect topic
aruco_detect = rospy.Subscriber('aruco_detect/markers', MarkerArray, markers_callback)

# Wait until the marker is detected
timeout = rospy.Time.now() + rospy.Duration(5)
while not marker_detected and rospy.Time.now() < timeout:
    rospy.sleep(0.5)

# If marker is not detected, land
if not marker_detected:
    print("Marker not detected, landing...")
    rospy.sleep(30)
    res = land()
    if res.success:
        print('Drone is landing due to timeout')
    sys.exit(0)

# Align the drone with the aruco marker
navigate_wait(x=0, y=0, z=0.4, yaw=0.0, speed=0.1, frame_id='aruco_119')
print('Move 1 complete')

# Move 30 cm back along y-axis to "pick up payload"
navigate_wait(x=0, y=-0.3, z=0.4, speed=0.1, frame_id='aruco_119')
print('Move 2 complete')

# Lift 10 cm above
navigate_wait(x=0, y=0, z=0.1, frame_id='body')
print('Move 3 complete')

# Return to above the aruco map 
tel = get_telemetry(frame_id='body')
navigate_wait(x=0, y=0.3, z=tel.z, frame_id='body')
print('Move 4 complete')

rospy.sleep(30)
print("Mission successful")

res = land()

if res.success:
    print('drone is landing')

