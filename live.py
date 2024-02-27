from lib.epd2in13_V4 import EPD, epdconfig
from PIL import Image, ImageDraw
from picamera import PiCamera
from time import sleep
import numpy as np
import logging
from sys import exit

#logging.basicConfig(level=logging.DEBUG)

def init():
    # Prep screen
    logging.debug("init screen")
    epd = EPD()
    epd.init()
    epd.Clear(0xff)
    img = Image.new("1", (epd.height, epd.width), 255)

    # Prep camera
    logging.debug("init camera")
    cam = PiCamera()

    return epd, cam, img

def capture(cam):
    # Capture image 
    logging.debug("capture picture")
    cam.capture("cap.jpg")
    cap = Image.open("cap.jpg")
    
    # resize (720 x 480) -> (250, 122)
    # 720/2.88=250, 480/2.88=166.66
    logging.debug("resize")
    cap.thumbnail((250, 167), Image.LANCZOS)
    return cap

def main():
    epd, cam, img = init()

    try:
        while 1:
            cap = capture(cam)

            # grayscale
            cap.convert("L")
            box = (0, 25, epd.height, epd.width)

            # BMP
            logging.debug("BMP")
            img.paste(cap)
            epd.display(epd.getbuffer(img))
            
            # save
            img.save("wat.bmp")
    except KeyboardInterrupt:
        epdconfig.module_exit(cleanup=True)


if __name__ == "__main__":
    main()
