import torch
from torch.nn import functional as F
from detoxify import Detoxify
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


class ToxicContentClassifier:
    _instance = None

    @staticmethod
    def get_instance():
        if ToxicContentClassifier._instance is None:
            ToxicContentClassifier._instance = ToxicContentClassifier()
        return ToxicContentClassifier._instance

    def __init__(self):
        if ToxicContentClassifier._instance is not None:
            raise Exception(
                "This is a singleton class, use the get_instance() method.")

        self.model = Detoxify("multilingual")

    @torch.no_grad()
    def predict(self, text: str):
        prediction = self.model.predict(text)
        offensive_entries = [{"label": key, "score": float(value)} for key,
                             value in prediction.items() if value > 0.8]
        if offensive_entries:
            offensive_entries_text = [f"{int(value.get("score") * 100)}% of {value.get("label", "").capitalize()}" for
                                      value in offensive_entries]
            return {
                "status": True,
                "reason": f"The content provided has toxic elements associated with it with: {", ".join(offensive_entries_text)}",
                "labels": offensive_entries,
                "toxic": True
            }
        else:
            return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None, "toxic": False}


class TamilToxicContentClassifier:
    _instance = None

    @staticmethod
    def get_instance(model_name="Hate-speech-CNERG/deoffxlmr-mono-tamil"):
        if TamilToxicContentClassifier._instance is None:
            TamilToxicContentClassifier._instance = TamilToxicContentClassifier(
                model_name)
        return TamilToxicContentClassifier._instance

    def __init__(self, model_name):
        if TamilToxicContentClassifier._instance is not None:
            raise Exception(
                "This is a singleton class, use the get_instance() method.")
        self.pipeline = pipeline("text-classification", model=model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt",
                                truncation=True, padding=True)
        outputs = self.model(**inputs)
        result = self.pipeline(text)[0]
        match result:
            case "Not_offensive":
                return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None, "toxic": False}
            case "Off_target_other":
                return {"status": True, "reason": "The content provided has toxic elements associated with it, aiming at offending other parties.", "labels": [result], "toxic": True}
            case "Profanity":
                return {"status": True, "reason": "The content provided has toxic elements associated with it as it uses profane language.", "labels": [result], "toxic": True}
            case _:
                return {"status": True, "reason": "The content provided has toxic elements associated with it as it contains offensive entities.", "labels": [result], "toxic": True}
