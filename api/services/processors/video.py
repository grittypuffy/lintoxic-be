import cv2
import os
import sys
import numpy as np
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from dotenv import load_dotenv
import multiprocessing
import glob

from lintoxic.utils.audio import AudioProcessor

load_dotenv()


class VideoProcessor:
    _instance = None

    @staticmethod
    def get_instance():
        if VideoProcessor._instance is None:
            VideoProcessor._instance = VideoProcessor()
        return VideoProcessor._instance

    def __init__(self):
        if VideoProcessor._instance is not None:
            raise Exception(
                "This is a singleton class, use the get_instance() method.")
        self.audio_processor = AudioProcessor.get_instance()
        self.image_processor = NSFWImageClassificationModel()

    def create_temporary_folder(self, temp_dir_name=None):
        preprocessing_dir = os.getenv("PREPROCESSING_DIR") if os.getenv(
            "PREPROCESSING_DIR") else os.path.join(Path.home(), "lintoxic", "preprocessing")
        temp_dir_path = os.path.join(preprocessing_dir, temp_dir_name)
        os.makedirs(temp_dir_path, exist_ok=True)
        return temp_dir_path

    def extract_frames(self, video_path, frames_dir):
        video_capture = cv2.VideoCapture(video_path)
        success, frame = video_capture.read()
        frame_count = 0
        saved_frame_count = 0
        save_next_frame = False

        while success:
            if save_next_frame:
                frame_file = os.path.join(
                    frames_dir, f"frame_{saved_frame_count}.jpg")
                cv2.imwrite(frame_file, frame)
                saved_frame_count += 1
                save_next_frame = False
            else:
                if frame_count % 60 == 0:
                    save_next_frame = True

            success, frame = video_capture.read()
            frame_count += 1

        video_capture.release()
        print(f"Total frames: {frame_count}, Saved frames: {
              saved_frame_count}")

    def extract_text_from_images(self, images_dir):
        image_files = glob.glob(os.path.join(images_dir, "*.jpg"))
        num_workers = min(multiprocessing.cpu_count(), 8)
        text_list = set()
        for image_file in image_files:
            text_list.add(extract_text_from_image(image_file))
        return "".join(list(text_list))

    def process_video(self, path: str):
        temporary_directory_id = datetime.now().strftime("%Y%m%d%H%M%S")
        frames_dir = self.create_temporary_folder(temporary_directory_id)
        self.extract_frames(path, images_session_dir)
        return self.extract_text_from_images(images_session_dir)
