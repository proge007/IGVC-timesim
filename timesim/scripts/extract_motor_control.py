from pathlib import Path

import numpy as np

from mcap.reader import make_reader 
from mcap_ros2.decoder import DecoderFactory

bag_path = (
    Path.home()
    /"timesim-DATA"
    /"bags"
    /"rosbag2_2025_05_28-00_54_27"
    /"rosbag2_2025_05_28-00_54_27_0.mcap"
)


output_path = (
    Path.home()
    / "timesim-DATA"
    / "extracted"
    / "test01"
    / "motor.npy"
)


motor_dict = {}

with bag_path.open("rb") as bag_file:
    reader = make_reader(
        bag_file,
        decoder_factories=[DecoderFactory()]
    )

    motor_messages = reader.iter_decoded_messages(
        topics=["/motor_control"]
    )

    for schema, channel, message, motor in motor_messages:
        
        timestamp = message.log_time / 1e9

        motor_dict[timestamp] = [
            motor.throttle,
            motor.steering
        ]


np.save(output_path, motor_dict)


print("motor control data extract complete")
print("motor messages:", len(motor_dict))
print("saved to:", output_path)


    