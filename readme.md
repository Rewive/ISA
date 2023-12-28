# 🎉 ISA: ImageEncoderDecoder 🎉

`ISA` - это 🚀 мощная Python библиотека для кодирования и декодирования изображений. Она предоставляет самый безопасный способ шифрования изображений.

![Image1](shuffled/shuffled.png)![Image2](out/original.png)

## 📦 Установка

Скопируйте файл `main.py` в свой проект и `run.py` в качестве примера использования кода.

## 🚀 Использование

```python
from main import ImageEncoderDecoder

# Создание экземпляра класса ImageEncoderDecoder
encoder_decoder = ImageEncoderDecoder('Ваш пароль')

# Кодирование изображения
result = encoder_decoder.encode_image('input/go.jpg')
result['image'].save('shuffled/shuffled.png', pnginfo=result['metadata'])

# Декодирование изображения
original_img = encoder_decoder.decode_image('shuffled/shuffled.png')
original_img.save('original.png')
```

## 📚 Документация

### Класс `ImageEncoderDecoder`

#### `__init__(self, password: str)`

Конструктор класса `ImageEncoderDecoder`. Принимает аргумент `password` в качестве строки.

#### `encode_image(self, img_path: str) -> dict`

Метод для кодирования изображения. Принимает путь к изображению в качестве строки. Возвращает словарь, содержащий закодированное изображение и метаданные.

#### `decode_image(self, shuffled_img_path: str) -> Image`

Метод для декодирования изображения. Принимает путь к закодированному изображению в качестве строки. Возвращает декодированное изображение.

## 📜 Лицензия

[MIT](https://choosealicense.com/licenses/mit/)