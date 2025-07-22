from meme_service.add_meme_text import add_text_to_image
from meme_service.create_image import create_image
from meme_service.meme_creator import phrase_generator
from meme_service.text_translater import translate_to_english, translate_to_russian


def create_meme(text: str) -> str:
    en_text = translate_to_english(text)
    meme_theme = phrase_generator(en_text)
    img_name = create_image(meme_theme)
    ru_text = translate_to_russian(meme_theme)
    new_img_name = f'{img_name.split('.')[0]}_meme.png'
    add_text_to_image(
        input_image_path=img_name,
        output_image_path=new_img_name,
        text=ru_text,
    )
    return new_img_name
