import logging
from services.processors.toxicity.classifier import ToxicContentClassifier, TamilToxicContentClassifier


def check_toxicity(text: str):
    toxic_content_classifier: ToxicContentClassifier = ToxicContentClassifier.get_instance()
    result = toxic_content_classifier.predict(text)

    if result.get("status"):
        return result

    tamil_toxic_content_classifier: TamilToxicContentClassifier = TamilToxicContentClassifier.get_instance()
    result = tamil_toxic_content_classifier.predict(text)

    if result.get("status"):
        return result

    return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None}
