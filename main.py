from flask import Flask
import time
import random
from rpi_ws281x import *
import argparse
import mido

LED_COUNT = 240
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 65
LED_INVERT = False
LED_CHANNEL = 0

app = Flask(__name__)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/rainbow')
def rainbow():
    try:
        while True:
            print('rainbow')
            rainbow(strip)
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)

    return 'Rainbow!'


def color_wipe(strip, color, wait_ms=50, iterations=10):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + p, color)
        strip.show()
        time.sleep(wait_mx / 1000.0)
        for i in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i + q, 0)


def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wasi_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
    strip.show()


def rainbowCycle(strip, wait_ms=20, iterations=5):
    for j in range(256 * iterations):
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def note(strip, msg, wait_ms=20):
    if msg.note - 20 < 29:
        print(f'<29: {msg.note * 3, 255 - msg.note * 3, 0}')
        strip.setPixelColor(msg.note, Color(msg.note * 3, 255 - msg.note * 3, 0))
    elif msg.note - 20 < 58:
        print(f'<58: {msg.note * 3, 0, 255 - msg.note * 3}')
        strip.setPixelColor(msg.note, Color(msg.note * 3, 0, 255 - msg.note * 3))
    else:
        print(f'else: {0, msg.note * 3, 255 - msg.note * 3}')
        strip.setPixelColor(msg.note, Color(0, msg.note * 3, 255 - msg.note * 3))

    # Calculate number of pixels or create pre calculated dict or something, ex: note 23 = pixels 20-30
    # 'Fade' Color out from nucleation pixel

    # strip.setPixelColor(msg.note, Color(red, green, blue))


def fade(strip, note, wait_ms=20):
    print('fade')
    # Fade pixel out


#       for i in range(max())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    with mido.open_input('ARIUS:ARIUS MIDI 1 20:0') as inport:
        for msg in inport:
            if msg.type == 'note_on':
                note(strip, msg)
                strip.show()
            else:
                fade(strip, msg)
