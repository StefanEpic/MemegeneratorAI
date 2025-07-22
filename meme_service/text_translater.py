from translate import Translator


def translate_to_english(text: str) -> str:
    translator = Translator(to_lang="en", from_lang="ru")
    translation = translator.translate(text)
    return translation if translation else text


def translate_to_russian(text: str) -> str:
    translator = Translator(to_lang="ru", from_lang="en")
    translation = translator.translate(text)
    return translation
