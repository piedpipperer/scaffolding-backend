import random
from captcha.image import ImageCaptcha
from PIL.Image import Image


def get_captcha() -> tuple[str, Image]:
    image = ImageCaptcha(width=100, height=40)
    captcha = "".join([str(random.randint(0, 9)) for _ in range(4)])
    # image.generate_image(captcha).save("captcha.png")
    return captcha, image.generate_image(captcha)
