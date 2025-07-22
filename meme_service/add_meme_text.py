from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(
        input_image_path,
        output_image_path,
        text,
        font_path="arial.ttf",
        font_size=36,
        text_color=(255, 255, 255),
        outline_color=(0, 0, 0),
        outline_width=2,
        position="bottom",
        margin=20
):
    # Открываем изображение
    image = Image.open(input_image_path)
    draw = ImageDraw.Draw(image)

    # Загружаем шрифт (если не найден, используем стандартный)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Рассчитываем максимальную ширину текста с учетом отступов
    max_width = image.width - 2 * margin

    # Функция для разбиения текста на строки с переносами
    def split_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # Проверяем ширину текущей строки с новым словом
            test_line = ' '.join(current_line + [word])
            left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
            test_width = right - left

            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

                # Проверяем, не слишком ли длинное само слово
                left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
                word_width = right - left
                if word_width > max_width:
                    # Если слово слишком длинное, разбиваем его
                    chars = list(word)
                    split_word = []
                    current_chars = []

                    for char in chars:
                        test_chars = ''.join(current_chars + [char])
                        left, top, right, bottom = draw.textbbox((0, 0), test_chars, font=font)
                        test_width = right - left

                        if test_width <= max_width:
                            current_chars.append(char)
                        else:
                            if current_chars:
                                split_word.append(''.join(current_chars))
                            current_chars = [char]

                    if current_chars:
                        split_word.append(''.join(current_chars))

                    lines.extend(split_word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    # Разбиваем текст на строки с переносами
    lines = split_text(text, font, max_width)

    # Рассчитываем общие размеры текста
    total_text_height = 0
    line_heights = []

    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        line_height = bottom - top
        line_heights.append(line_height)
        total_text_height += line_height

    # Определяем позицию текста
    if position == "bottom":
        y = image.height - total_text_height - margin
    else:
        y = margin

    # Рисуем текст с обводкой
    for i, line in enumerate(lines):
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        line_width = right - left
        x = image.width // 2  # Центр по горизонтали

        # Рисуем обводку (контур)
        for adj in range(outline_width):
            for x_adj in [-adj, adj]:
                for y_adj in [-adj, adj]:
                    draw.text((x + x_adj, y + y_adj), line, font=font,
                              fill=outline_color, anchor="mm")

        # Рисуем основной текст
        draw.text((x, y), line, font=font, fill=text_color, anchor="mm")

        # Переходим к следующей строке
        y += line_heights[i]

    # Сохраняем изображение
    image.save(output_image_path)
