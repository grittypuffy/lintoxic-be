from typing import Optional
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor


class NSFWImageClassificationModel:
    _instance = None

    @staticmethod
    def get_instance(model_name: str = "Falconsai/nsfw_image_detection"):
        if NSFWImageClassificationModel._instance is None:
            NSFWImageClassificationModel._instance = NSFWImageClassificationModel(
                model_name)
        return NSFWImageClassificationModel._instance

    def __init__(self, model_name: str = "Falconsai/nsfw_image_detection"):
        if NSFWImageClassificationModel._instance is not None:
            raise Exception(
                "This is a singleton class, use the get_instance() method.")

        self.model = AutoModelForImageClassification.from_pretrained(
            model_name)
        self.processor = ViTImageProcessor.from_pretrained(model_name)

    def predict(self, image_path: str):
        img = Image.open(image_path)
        inputs = self.processor(images=img, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_label = logits.argmax(-1).item()
        if predicted_label:
            return {"status": True if predicted_label else False, "reason": f"The content is not safe for work and is classified under the following label: {self.model.config.id2label[predicted_label]}", "labels": [{"label": self.model.config.id2label[predicted_label]}], "nsfw": True}
        else:
            return {"status": True if predicted_label else False, "reason": f"The content is safe for work.", "labels": None, "nsfw": False}
