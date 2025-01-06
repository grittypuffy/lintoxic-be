from typing import Optional
import torch
import speech_recognition as sr
from transformers import MBartForConditionalGeneration, MBartTokenizer
from lingua import Language, LanguageDetectorBuilder, IsoCode639_1


class AudioProcessor:
    _instance = None

    @staticmethod
    def get_instance():
        if AudioProcessor._instance is None:
            AudioProcessor._instance = AudioProcessor()
        return AudioProcessor._instance

    def __init__(self, model_name: str = "facebook/mbart-large-50-many-to-one-mmt"):
        if AudioProcessor._instance is not None:
            raise Exception(
                "This is a singleton class, use the get_instance() method.")
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MBartTokenizer.from_pretrained(model_name)
        self.languages = [Language.ENGLISH, Language.FRENCH,
                          Language.GERMAN, Language.SPANISH, Language.TAMIL]
        self.language_detector = LanguageDetectorBuilder.from_languages(
            *self.languages).build()

    @torch.no_grad()
    def predict_language(self, text: str) -> str:
        confidence_value = self.language_detector.compute_language_confidence_values(text)[
            0]
        if confidence_value is not None:
            return confidence_value.language.iso_code_639_1
        return None

    def translate_text(self, text: str, source_lang: str) -> str:
        self.tokenizer.src_lang = source_lang
        encoded_text = self.tokenizer(text, return_tensors="pt")

        # Perform translation
        generated_tokens = self.model.generate(
            **encoded_text
        )

        translated_text = self.tokenizer.decode(
            generated_tokens[0], skip_special_tokens=True)
        return {"translation": translated_text}

    def speech_to_text(self, file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_text = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_text)
                return {"transcription": transcription}
            except:
                return {"error": "An error occured during transcription"}

    def process_audio(self, file: str, target_lang: str = 'en_XX'):
        transcription = self.speech_to_text(file)
        if transcription.get("error"):
            return {"error": "Unable to get the transcription for the given audio"}

        detected_lang = self.predict_language(
            transcription.get("transcription"))
        if detected_lang == IsoCode639_1.EN:
            return transcription.get("transcription")

        if not detected_lang:
            return {"error": "Unable to detect language for the given transcription"}

        lang_mapping = {
            'en': 'en_XX',
            'fr': 'fr_XX',
            'de': 'de_XX',
            'es': 'es_XX',
            'ta': 'ta_IN'
        }

        source_lang_code = lang_mapping.get(detected_lang, 'en_XX')
        translated_text = self.translate_text(
            transcription.get("transcription"), source_lang_code)
        return {"transcription": translated_text.get("translation")}
