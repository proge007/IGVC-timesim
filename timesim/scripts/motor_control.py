from pathlib import Path
from mcap.reader import make_reader 
from mcap_ros2.decoder import DecoderFactory

bag_path = (
    Path.home()
    /"timesim-DATA"
    /"bags"
    /"rosbag2_2025_05_28-00_54_27"
    /"rosbag2_2025_05_28-00_54_27_0.mcap"
)

with bag_path.open("rb") as bag_file:
    reader = make_reader(
        bag_file,
        decoder_factories=[DecoderFactory()]
    )

    motor_messages = reader.iter_decoded_messages(
        topics=["/motor_control"]
    )

    for count, (schema, channel, message, motor) in enumerate(motor_messages):

        timestamp = message.log_time / 1e9
        print (
            f"time={timestamp:.6f} "
            f" throttle{motor.throttle} "
            f" steering={motor.steering}"
        )
        if count >= 4:
            break
        