from PIL import Image
import pytesseract
import re


def recognize_captcha(img_path):
    im = Image.open(img_path)
    verify_code = pytesseract.image_to_string(im)
    verify_code = re.sub('[^a-zA-Z]', '', verify_code)
    return verify_code


if __name__ == '__main__':
    res = recognize_captcha('verify.jpg')
    print(res)
