import asyncio
import cv2
import os
import uuid
import numpy as np
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import glob

from audio_extract import extract_audio

from api.config.environment import EnvVarConfig, get_env_config
from api.services.processors.image import extract_text
from api.services.processors.audio import AudioProcessor
from api.services.processors.nsfw.image import NSFWImageClassificationModel
from api.services.validate.audio import evaluate_audio
from api.services.validate.image import evaluate_image
from api.services.validate.text import evaluate_text

env: EnvVarConfig = get_env_config()


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
        os.makedirs(env.preprocessing_dir, exist_ok=True)

    def create_temporary_folder(self, temp_dir_name: str):
        preprocessing_dir = env.preprocessing_dir
        temp_dir_path = os.path.join(preprocessing_dir, temp_dir_name)
        os.makedirs(temp_dir_path, exist_ok=True)
        return temp_dir_path

    def extract_frames(self, video_path: str, frames_dir: str):
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

    def extract_text_from_images(self, images_dir: str):
        image_files = glob.glob(os.path.join(images_dir, "*.jpg"))
        num_workers = min(multiprocessing.cpu_count(), 8)
        text_list = set()
        for image_file in image_files:
            text_list.add(extract_text(image_file))
        return "".join(list(text_list))

    async def evaluate_images(self, images_dir: str):
        image_files = glob.glob(os.path.join(images_dir, "*.jpg"))
        num_workers = min(multiprocessing.cpu_count(), 8)
        for image_file in image_files:
            result = await evaluate_image(image_file)
            if result.get("status"):
                return result

        return {"status": False, "reason": "The contents provided does not have any toxic elements, NSFW content or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}

    def extract_audio_from_video(self, video_path: str, temp_dir_name: str):
        try:
            audio_path = os.path.join(
                env.preprocessing_dir, temp_dir_name, "audio.wav")
            _ = extract_audio(input_path=video_path,
                              output_path=audio_path, output_format="wav")
            return audio_path
        except Exception as e:
            print(e)
            return None

    async def process_video(self, path: str):
        temporary_directory_id = str(uuid.uuid4())
        frames_dir = self.create_temporary_folder(temporary_directory_id)
        self.extract_frames(path, frames_dir)
        text = self.extract_text_from_images(frames_dir)
        audio_path = self.extract_audio_from_video(
            path, temporary_directory_id)
        if audio_path:
            results = await asyncio.gather(
                evaluate_text(text),
                evaluate_audio(audio_path),
                self.evaluate_images(frames_dir)
            )
            for result in results:
                if result.get("status"):
                    return result

            return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
        else:
            results = await asyncio.gather(
                evaluate_text(text),
                self.evaluate_images(frames_dir)
            )
            for result in results:
                if result.get("status"):
                    return result

            return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
