import os

from app.logger_client import LoggerClient
from app.utils import get_random_string
from PIL import Image, ImageFont, ImageDraw 

class ImageMaker():
    def __init__(self, config: dict, logger: LoggerClient):
        self._config = config.IMAGE_MAKER_CONFIG
        self._logger = logger

        filepath = os.path.abspath(os.path.dirname(__file__))
        parentpath = os.path.abspath(os.path.join(filepath, os.pardir))
        self._media_folder = os.path.join(parentpath, self._config["media_folder"])

        self._image_folder = self._config["expendable_images_folder"]
        if not os.path.exists(self._image_folder):
            os.mkdir(self._image_folder)

    def create_image(self, text, level):
        text = text[:8].center(8, ' ').upper()
        level = self._get_level(level)
        if not level:
            return None  # Fallo, algun listo le ha pasado string

        exp_image = Image.open(os.path.join(self._media_folder, 'background.jpg'))
        font = ImageFont.truetype(os.path.join(self._media_folder, 'Motor.ttf'), 55)

        image_editable = ImageDraw.Draw(exp_image)
        image_editable.text((14,60), f'{text} {level}', (237, 230, 211), font=font)

        image_path = os.path.join(self._image_folder, f'{get_random_string()}.jpg')
        exp_image.save(image_path)
        self._logger.info(f'Image saved at {image_path}')

        return image_path

    def _get_level(self, level):
        level = self._is_number(level)
        if not level:
            return None

        level = self._cap_number(level)
        if isinstance(level, float):
            return str("{:.2f}".format(level)).ljust(6, ' ')
        return str(level).ljust(6, ' ')

    def _is_number(self, level):
        try:
            return int(level)
        except ValueError:
            pass

        try:
            return float(level)
        except ValueError:
            return None

    def _cap_number(self, level):
        if level > 100:
            return 100
        elif level < -100:
            return -100
        else:
            return level
