import os
import cv2
import torch
import numpy as np
import pandas as pd

from torch.utils.data import Dataset


class FusionDataset(Dataset):

    def __init__(self, root_dir):

        self.root_dir = root_dir

        self.cam0_dir = os.path.join(root_dir, "cam0")
        self.cam1_dir = os.path.join(root_dir, "cam1")
        self.lidar_dir = os.path.join(root_dir, "lidar")

        print("Loading dataset:", root_dir)

        # Camera files
        self.cam0_files = sorted(
            [f for f in os.listdir(self.cam0_dir)
             if f.endswith(".jpg")]
        )
        print(len(self.cam0_files))

        self.cam1_files = sorted(
            [f for f in os.listdir(self.cam1_dir)
             if f.endswith(".jpg")]
        )

        # LiDAR files
        self.lidar_files = sorted(
            [f for f in os.listdir(self.lidar_dir)
             if f.endswith(".csv")]
        )

        # IMU
        self.imu_df = pd.read_csv(
            os.path.join(root_dir, "imu.csv"),
            header=None
        )

        # Steering + Throttle
        self.joy_df = pd.read_csv(
            os.path.join(root_dir, "joy.csv"),
            header=None
        )

        # Use shortest modality length
        self.length = min(
            len(self.cam0_files),
            len(self.cam1_files),
            len(self.lidar_files),
            len(self.imu_df),
            len(self.joy_df)
        )

        print(f"Dataset size: {self.length}")

    def __len__(self):
        return self.length

    def __getitem__(self, idx):

        # ==========================
        # CAMERA 0
        # ==========================
        img0_path = os.path.join(
            self.cam0_dir,
            self.cam0_files[idx]
        )

        img0 = cv2.imread(img0_path)

        if img0 is None:
            raise RuntimeError(
                f"Missing image: {img0_path}"
            )

        img0 = cv2.resize(img0, (224, 224))

        img0 = torch.tensor(
            img0,
            dtype=torch.float32
        ).permute(2, 0, 1) / 255.0

        # ==========================
        # CAMERA 1
        # ==========================
        img1_path = os.path.join(
            self.cam1_dir,
            self.cam1_files[idx]
        )

        img1 = cv2.imread(img1_path)

        if img1 is None:
            raise RuntimeError(
                f"Missing image: {img1_path}"
            )

        img1 = cv2.resize(img1, (224, 224))

        img1 = torch.tensor(
            img1,
            dtype=torch.float32
        ).permute(2, 0, 1) / 255.0

        # ==========================
        # LiDAR
        # ==========================
        lidar_path = os.path.join(
            self.lidar_dir,
            self.lidar_files[idx]
        )

        lidar = np.loadtxt(
            lidar_path,
            delimiter=","
        ).astype(np.float32)

        lidar[np.isnan(lidar)] = 0.0
        lidar[np.isinf(lidar)] = 0.0

        lidar = np.clip(
            lidar,
            0.0,
            50.0
        )

        lidar = lidar / 50.0

        lidar = torch.tensor(
            lidar,
            dtype=torch.float32
        )

        # ==========================
        # IMU
        # ==========================
        '''imu = torch.tensor(
            self.imu_df.iloc[idx].values,
            dtype=torch.float32
        )'''
        imu = self.imu_df.iloc[idx].values.astype(np.float32)
        imu = np.nan_to_num(
            imu,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        imu = torch.tensor(
            imu,
            dtype=torch.float32
        )

        # ==========================
        # LABEL
        # ==========================
        label = torch.tensor(
            self.joy_df.iloc[idx].values,
            dtype=torch.float32
        )

        return (
            img0,
            img1,
            lidar,
            imu,
            label
        )