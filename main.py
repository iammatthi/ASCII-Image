import numpy as np
import sys

from PIL import Image


def openImage(filename):
    # Open image with Pillow
    image = Image.open(filename)

    # Convert to 8-bit pixels, black and white (grey scale)
    grey_scale_image = image.convert(mode="L")

    # Convert Pillow image to NumPy array
    return np.nan_to_num(np.asarray(grey_scale_image))


def compressImage(img, rows=None, cols=None):
    height, width = img.shape

    if rows is None and cols is None:
        ratio = width / height
        max_chars = 200
        if ratio >= 1:
            cols = max_chars
            rows = int(cols / ratio)
        else:
            rows = max_chars
            cols = int(rows * ratio)
        # 45% of the row height removed because it is greater than the width of a character
        rows = int(rows * 0.55)

    print(f'Cols: {cols}')
    print(f'Rows: {rows}')

    cell_width = width / cols
    cell_height = height / rows

    ascii_array = []

    for i in range(0, rows):
        row_ascii_array = []
        for j in range(0, cols):
            grey_mean = np.mean(
                img[int(i * cell_height):min(int((i + 1) * cell_height), height),
                    int(j * cell_width):min(int((j + 1) * cell_width), width)]
            )
            row_ascii_array.append(grey_scale_to_ascii(
                grey=grey_mean, advanced=False))

        ascii_array.append(row_ascii_array)

    return ascii_array


def grey_scale_to_ascii(grey, advanced=False):
    simple_chars = ' .:-=+*#%@'
    advanced_chars = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

    chars = advanced_chars if advanced else simple_chars
    return chars[min(int((grey / 255) * len(chars)), len(chars) - 1)]


def ascii_array_to_string(ascii_array):
    result = ""
    for row in ascii_array:
        for pixel in row:
            result += pixel

        result += "\n"

    return result


def main():
    path = input("Image path: ")
    img = openImage(filename=path)

    ascii_array = compressImage(img=img)

    print(ascii_array_to_string(ascii_array))


if __name__ == '__main__':
    main()
