import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import cv2
import os


class FusionDataset(Dataset):

    def __init__(self, root_dir, csv_file):

        self.root_dir = root_dir

        csv_path = os.path.join(root_dir, csv_file)

        print("Loading CSV:", csv_path)

        self.df = pd.read_csv(csv_path)

        # Load sensor dictionaries
        raw_lidar = np.load(
            os.path.join(root_dir, "lidar.npy"),
            allow_pickle=True
        ).item()

        self.lidar_dict = {}

        for ts, scan in raw_lidar.items():

            scan = np.array(scan, dtype=np.float32)

            # Replace inf values
            scan[np.isinf(scan)] = 0.0

            # Replace NaNs
            scan[np.isnan(scan)] = 0.0

            # Optional normalization (VERY IMPORTANT)
            scan = np.clip(scan, 0.0, 50.0)   # max lidar range ≈ 50m
            scan = scan / 50.0                # normalize 0–1

            self.lidar_dict[ts] = scan

        self.imu_dict = np.load(
            os.path.join(root_dir, "imu.npy"),
            allow_pickle=True
        ).item()

        print("Sensor dictionaries loaded.")

    # -----------------------------
    # timestamp matching
    # -----------------------------
    def nearest_timestamp(self, target, source_dict):

        keys = np.array(list(source_dict.keys()), dtype=float)
        target = float(target)

        idx = np.argmin(np.abs(keys - target))

        return keys[idx]

    # -----------------------------
    # fix camera paths
    # -----------------------------
    def fix_path(self, path):

        path = path.replace("cam0", "usb_cam_0_image_raw")
        path = path.replace("cam1", "usb_cam_1_image_raw")

        return path

    # -----------------------------
    # length
    # -----------------------------
    def __len__(self):
        return len(self.df)

    # -----------------------------
    # get item
    # -----------------------------
    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        # ========= CAMERA 0 =========
        img0_path = self.fix_path(row["cam0"])
        img0 = cv2.imread(img0_path)

        if img0 is None:
            raise RuntimeError(f"Missing image: {img0_path}")

        img0 = cv2.resize(img0, (224, 224))
        img0 = torch.tensor(img0).permute(2, 0, 1).float() / 255.0

        # ========= CAMERA 1 =========
        img1_path = self.fix_path(row["cam1"])
        img1 = cv2.imread(img1_path)

        if img1 is None:
            raise RuntimeError(f"Missing image: {img1_path}")

        img1 = cv2.resize(img1, (224, 224))
        img1 = torch.tensor(img1).permute(2, 0, 1).float() / 255.0

        # ========= LIDAR =========
        lidar_key = self.nearest_timestamp(
            row["lidar_ts"],
            self.lidar_dict
        )

        lidar = torch.tensor(
            self.lidar_dict[lidar_key],
            dtype=torch.float32
        )

        # ========= IMU =========
        imu_key = self.nearest_timestamp(
            row["imu_ts"],
            self.imu_dict
        )

        imu = torch.tensor(
            self.imu_dict[imu_key],
            dtype=torch.float32
        )

        # ========= LABEL =========
        label = torch.tensor([
            row["steer"],
            row["throttle"]
        ], dtype=torch.float32)

        return img0, img1, lidar, imu, label
