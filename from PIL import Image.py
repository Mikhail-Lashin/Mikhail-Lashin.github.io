from PIL import Image
import math

def remove_multiple_colors(input_path, output_path, colors_to_remove, tolerance=30):
    """
    Удаляет несколько заданных цветов и близкие к ним оттенки с изображения.

    :param input_path: Путь к входному изображению.
    :param output_path: Путь для сохранения выходного PNG-изображения.
    :param colors_to_remove: Список кортежей [(R, G, B), ...], содержащий цвета для удаления.
    :param tolerance: Допустимое "расстояние" от целевых цветов.
    """
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {input_path}")
        return

    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    for item in datas:
        pixel_to_remove = False
        # Проверяем, близок ли пиксель к какому-либо из цветов в нашем списке
        for target_color in colors_to_remove:
            r_target, g_target, b_target = target_color

            dist = math.sqrt(
                (item[0] - r_target)**2 +
                (item[1] - g_target)**2 +
                (item[2] - b_target)**2
            )

            # Если нашли совпадение с допуском, помечаем пиксель на удаление и выходим из внутреннего цикла
            if dist <= tolerance:
                pixel_to_remove = True
                break
        
        # Если пиксель был помечен, делаем его прозрачным
        if pixel_to_remove:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Фон успешно удален. Изображение сохранено как {output_path}")


# --- Пример использования ---
if __name__ == "__main__":
    # 1. Укажите правильные пути к файлам. Не забудьте 'r' перед строкой!
    input_image_path = r"C:\Users\t9169\Desktop\optim.png"  # <-- ВАШ ПУТЬ
    output_image_path = r"C:\Users\t9169\Desktop\optim_no_bg.png" # <-- ВАШ ПУТЬ

    # 2. Создаем список цветов, которые нужно удалить
    #    Первый - это светло-серый фон, второй - чисто белый.
    background_colors = [
        (217, 219, 222),  # Светло-серый/голубоватый фон
        (255, 255, 255)   # Чисто белый цвет
    ]

    # 3. Подберите допуск. Значение около 40-50 должно хорошо сработать для обоих цветов.
    #    Оно достаточно большое, чтобы захватить вариации серого, и легко покроет чисто белый.
    color_tolerance = 45

    remove_multiple_colors(
        input_image_path,
        output_image_path,
        background_colors,
        color_tolerance
    )