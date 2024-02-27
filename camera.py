from gpiozero import Button
from lib.epd2in13_V4 import EPD, epdconfig
from PIL import Image, ImageDraw, ImageFont
from picamera import PiCamera
from time import strftime, sleep
import numpy as np
import logging
from sys import exit
from tempfile import TemporaryFile
import glob

#logging.basicConfig(level=logging.DEBUG)

def init():
    # Prep screen
    logging.debug("init screen")
    epd = EPD()
    epd.init()
    #epd.Clear(0xff)
    img = Image.new("1", (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=18)
    box = [(50, 50), (205, 80)]
    draw.rectangle(box, fill=0, outline=0)
    draw.text((55, 55), "CAMERA READY", font=font, fill=255)
    epd.displayPartBaseImage(epd.getbuffer(img))

    # Prep camera
    logging.debug("init camera")
    cam = PiCamera()
    cam.rotation = 270

    return epd, cam, img

def capture(cam, format="bmp"):
    # Capture image 
    file = TemporaryFile()
    logging.debug("capture picture")
    cam.capture(file, format=format, resize=(250, 167), thumbnail=None)
    cap = Image.open(file)
    
    # resize (720 x 480) -> (250, 122)
    # 720/2.88=250, 480/2.88=166.66
    #logging.debug("resize")
    #cap.thumbnail((250, 167), Image.LANCZOS)
    return cap

def main():
    epd, cam, img = init()

    button = Button(21)

    try:
        while 1:
            #input("next pic")
            button.wait_for_press()
            cap = capture(cam)

            # grayscale
            cap.convert("L")
            box = (0, 25, epd.height, epd.width)

            # BMP
            logging.debug("BMP")
            img.paste(cap)
            epd.display(epd.getbuffer(img))
            
            # save
            name = strftime("%Y-%m-%d-%H:%M:%S")
            img.save(f"pics/{name}.bmp")
    except KeyboardInterrupt:
        epdconfig.module_exit(cleanup=True)


if __name__ == "__main__":
    main()
