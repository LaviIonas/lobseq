import struct
from array import array
import numpy as np

def read_labels(label_file):
    labels = []
    with open(label_file, 'rb') as f:
            magic, size = struct.unpack(">II", f.read(8))

            labels = array("B", f.read())

    return labels

def read_images(image_file):
    with open(image_file, 'rb') as f:
        magic, size, rows, cols = struct.unpack(">IIII", f.read(16))
        image_data = np.frombuffer(f.read(), dtype=np.uint8)
        images = image_data.reshape(size, rows, cols)

    return images