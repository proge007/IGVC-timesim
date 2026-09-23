import os
import cv2
import numpy as np

from rclpy.serialization import deserialize_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions

from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Joy
from cv_bridge import CvBridge

# =============================
# CONFIG
# =============================

#BAG_PATH = "/media/sf_E_DRIVE/rosbag2_2025_05_28-00_54_27"   # folder containing mcap
#BAG_PATH = "/media/sf_D_DRIVE/rosbag2_2025_05_28-00_54_27" 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--bag")
parser.add_argument("--output")

args = parser.parse_args()

BAG_PATH = args.bag
DATASET_DIR = args.output

CAMERA_TOPICS = [
    "/usb_cam_0/image_raw",
    "/usb_cam_1/image_raw"
]




LIDAR_TOPIC = "/scan"
IMU_TOPIC = "/imu/data"
CONTROL_TOPIC = "/joy"


###for quick test
MAX_CAM0_FRAMES = 1500


#DATASET_DIR = "dataset/05_28_27"
IMAGE_DIR = f"{DATASET_DIR}/images"

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

os.makedirs(f"{IMAGE_DIR}/cam_0", exist_ok=True)
os.makedirs(f"{IMAGE_DIR}/cam_1", exist_ok=True)


bridge = CvBridge()

lidar_data = []
imu_data = []
control_data = []

cam0_dict = {}
cam1_dict = {}
lidar_dict = {}
imu_dict = {}
joy_dict = {}

image_counts = {cam:0 for cam in CAMERA_TOPICS}

# =============================
# OPEN BAG
# =============================

reader = SequentialReader()

storage_options = StorageOptions(
    uri=BAG_PATH,
    storage_id="mcap"
)

converter_options = ConverterOptions(
    input_serialization_format="cdr",
    output_serialization_format="cdr"
)

reader.open(storage_options, converter_options)

topic_types = reader.get_all_topics_and_types()

type_map = {topic.name: topic.type for topic in topic_types}

# =============================
# READ BAG
# =============================

while reader.has_next():

    topic, data, timestamp = reader.read_next()

    # CAMERA

    if topic == "/usb_cam_0/image_raw":    

        msg = deserialize_message(data, Image)

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        cv_img = bridge.imgmsg_to_cv2(msg, "bgr8")

        filename = f"{IMAGE_DIR}/cam0/{image_counts[topic]:06d}.png"

        cv2.imwrite(filename, cv_img)

        cam0_dict[timestamp] = filename

        image_counts[topic] += 1

        ###added for testing
        if image_counts[topic] >= MAX_CAM0_FRAMES:
           print("test extraction frames limits completed")
           break

    elif topic == "/usb_cam_1/image_raw":

        msg = deserialize_message(data, Image)

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        cv_img = bridge.imgmsg_to_cv2(msg, "bgr8")

        filename = f"{IMAGE_DIR}/cam1/{image_counts[topic]:06d}.png"

        cv2.imwrite(filename, cv_img)

        cam1_dict[timestamp] = filename

        image_counts[topic] += 1
    # LIDAR
    elif topic == LIDAR_TOPIC:

        msg = deserialize_message(data, LaserScan)

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        lidar_dict[timestamp] = np.array(msg.ranges)
        '''ranges = np.array(msg.ranges)

        lidar_data.append(
            [timestamp] + ranges.tolist()
        )'''

    # IMU
    elif topic == IMU_TOPIC:

        msg = deserialize_message(data, Imu)

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        imu_dict[timestamp] = np.array([
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z,
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])
        '''msg = deserialize_message(data, Imu)

        imu_data.append([
            timestamp,
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z,
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])'''

    # MOTOR CONTROL
    elif topic == "/joy":

        msg = deserialize_message(data, Joy)

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        joy_dict[timestamp] = [
            msg.axes[0],
            msg.axes[1]
        ]
        '''elif topic == CONTROL_TOPIC:

        #msg = deserialize_message(data, type_map[topic])
        msg = deserialize_message(data, Joy)
        
        if len(msg.axes) < 2:
            continue

        timestamp = msg.header.stamp.sec + \
                msg.header.stamp.nanosec * 1e-9

        steering = msg.axes[0]
        throttle = msg.axes[1]

        control_data.append([timestamp, steering, throttle])'''

        # Convert to dict
        #msg_dict = {f.name: getattr(msg_generic, f.name) for f in msg_generic.__slots__}
        # Extract steering & throttle if they exist
        #steering = msg.axes[0]
        #throttle = msg.axes[1]
        #control_data.append([timestamp, steering, throttle])

# =============================
# SAVE DATA
# =============================

#np.save(f"{DATASET_DIR}/lidar.npy", np.array(lidar_data, dtype=object))
#np.save(f"{DATASET_DIR}/imu.npy", np.array(imu_data))
#np.save(f"{DATASET_DIR}/control.npy", np.array(control_data))

np.save(f"{DATASET_DIR}/cam0.npy", cam0_dict)
np.save(f"{DATASET_DIR}/cam1.npy", cam1_dict)
np.save(f"{DATASET_DIR}/lidar.npy", lidar_dict)
np.save(f"{DATASET_DIR}/imu.npy", imu_dict)
np.save(f"{DATASET_DIR}/joy.npy", joy_dict)

metadata = {
    "bag_path": BAG_PATH,
    "cam0_frames": len(cam0_dict),
    "cam1_frames": len(cam1_dict),
    "lidar_scans": len(lidar_dict),
    "imu_samples": len(imu_dict),
    "joy_samples": len(joy_dict)
}

np.save(
    f"{DATASET_DIR}/metadata.npy",
    metadata
)

print("Extraction Complete")


print("\nExtraction complete\n")

print("Camera frames:")
for cam in CAMERA_TOPICS:
    print(cam, image_counts[cam])

print("\nLiDAR:", len(lidar_data))
print("IMU:", len(imu_data))
print("Control:", len(control_data))

