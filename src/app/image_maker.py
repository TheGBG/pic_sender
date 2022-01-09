import os

from app.logger_client import LoggerClient
from app.utils import get_random_string
from PIL import Image, ImageFont, ImageDraw 

class ImageMaker():
    def __init__(self, config: dict, logger: LoggerClient):
        self._config = config.IMAGE_MAKER_CONFIG
        self._logger = logger

    def create_image(self, text, level):
        text = text[:10].center(10, ' ').upper()
        level = self._get_level(level)
        if not level:
            return None  # Fallo, algun listo le ha pasado string

        exp_image = Image.open(os.path.join(self._config['media_folder'], 'background.jpg'))
        font = ImageFont.truetype(os.path.join(self._config['media_folder'], 'Motor.ttf'), 45)

        image_editable = ImageDraw.Draw(exp_image)
        image_editable.text((14,60), f'{text} {level}', (237, 230, 211), font=font)

        image_path = os.path.join(self._config['image_folder'], f'{get_random_string()}.jpg')
        exp_image.save(image_path)
        return image_path

    def _get_level(self, level):
        level = self._is_num(level)
        if not level:
            return None

        level = self._cap_num(level)
        if isinstance(level, float):
            return str("{:.2f}".format(level)).center(7, ' ')
        return str(level).center(7, ' ')

    def _is_num(self, level):
        try:
            return int(level)
        except ValueError:
            pass

        try:
            return float(level)
        except ValueError:
            return None

    def _cap_num(self, level):
        if level >= 1000:
            return 999.99
        elif level <= -1000:
            return -999.99
        else:
            return level