from read_binary_data import read_images, read_labels
from extract_files import extract_files

from random import choice
import random
import numpy as np
import matplotlib.pyplot as plt

class lobseq():
    def __init__(self, directory):
        self.data = self.__get_training_data(extract_files(directory))
        self.X_train_raw = self.data[0]
        self.y_train_raw = self.data[1]
        self.X_test_raw = self.data[2]
        self.y_test_raw = self.data[3]

        self.y_train_map = {label: [] for label in range(10)}
        self.y_test_map = {label: [] for label in range(10)}
        self.__generate_label_map()

    def __get_training_data(self, file_dict):
        data = []

        # Read train images
        train_images = read_images(file_dict['train_images'])
        data.append(train_images)

        # Read train labels
        train_labels = read_labels(file_dict['train_labels'])
        data.append(train_labels)

        # Read test images
        test_images = read_images(file_dict['test_images'])
        data.append(test_images)

        # Read test labels
        test_labels = read_labels(file_dict['test_labels'])
        data.append(test_labels)

        return data
    
    def __generate_label_map(self):
        for index, label in enumerate(self.y_train_raw):
            self.y_train_map[label].append(index)
        
        for index, label in enumerate(self.y_test_raw):
            self.y_test_map[label].append(index)

    def __select_random_train_label(self, label):
        if self.y_train_map[label]:
            return choice(self.y_train_map[label])
        else:
            print(f"No images for the number {label} is available. \
                    Please try with a different number.")
            exit()
    
    def __select_random_test_label(self, label):
        if self.y_test_map[label]:
            return choice(self.y_test_map[label])
        else:
            print(f"No images for the number {label} is available. \
                    Please try with a different number.")
            exit()
    
    def __determine_bounds(self, digit, offset):
        left_bound = 0
        right_bound = 27

        # Find the left bound of the digit
        for i in range(28):
            if np.any(digit[:, i] != 1):
                left_bound = i - offset
                break

        # Find the right bound of the digit
        for i in range(27, -1, -1):
            if np.any(digit[:, i] != 1):
                right_bound = i + offset
                break

        return (left_bound, right_bound)

    """
    Can call this function for fun
    """
    def __uniform_image_sequence(self, sequence, offset, data_set):

        images = []
        bounds = []

        if data_set == 'train':
            for digit in sequence:
                img = self.X_train_raw[self.__select_random_train_label(digit)]
                bounds.append(self.__determine_bounds(img, offset))
                images.append(img)
        else:
            for digit in sequence:
                img = self.X_test_raw[self.__select_random_test_label(digit)]
                bounds.append(self.__determine_bounds(img, offset))
                images.append(img)
        
        return (images, bounds)
    
    def non_uniform_sequence(self, sequence, offset, canvas_inc, data_set):
        images = []
        bounds = []

        if data_set == 'train':
            images, bounds = self.__uniform_image_sequence(sequence, offset, 'train')
        elif data_set == 'test':
            images, bounds = self.__uniform_image_sequence(sequence, offset, 'test')
        else:
            raise ValueError("Wrong data set selected for sequence: expected data_set='train' or 'test'")

        h , w = 28, 28
        canvas_h = h + canvas_inc
        canvas_w = w + canvas_inc

        noisy_images = []

        for digit, (l_bound, r_bound) in zip(images, bounds):
            # Create an empty canvas for the image
            canvas = np.ones((canvas_h, canvas_w), dtype=np.float32)

            # Generate a Random vertical position
            y_pos = random.randint(0, 10)
            # Generate a Random horizontal position 
            x_pos = random.randint(-l_bound, canvas_w-r_bound)

            # Calculate the start and end of y
            y_start = y_pos
            y_end = y_start + h

            # x_pos could be positive or negative depending on if the image is being skewed left of right
            if x_pos < 0: # if skewed left
                # grab digit splice with the left part cut off
                digit = np.array(digit[:, -x_pos:])
                # paste splice on to canvas
                canvas[y_start:y_end, 0:digit.shape[1]] = digit
            elif w+x_pos > canvas_w: # if skewed right
                # grab digit splice with the right part cut off
                alpha = w + x_pos - canvas_w
                digit = digit[:, :w-alpha]
                # paste splice on to canvas
                canvas[y_start:y_end, x_pos:canvas_w] = digit
            else:
                # if no skew
                canvas[y_start:y_end, x_pos:x_pos+w] = digit

            # append canvas to array
            noisy_images.append(canvas)
        
        # stack the individual canvas together into a single image
        noisy_images = np.hstack(noisy_images)

        return noisy_images
    
    def generate_random_database(self, dataset_size, sequence_size, offset, canvas_inc, data_set='train'):
        if data_set == 'train' or data_set == 'test':
            pass
        else:
            raise ValueError("Wrong data set selected for sequence: expected data_set='train' or 'test'")
        
        dataset = []
        labels = []

        for i in range(dataset_size):
            sequence = np.random.randint(0,10, size=sequence_size)
            sequence_array = self.non_uniform_sequence(sequence, offset, canvas_inc, data_set)
            dataset.append(sequence_array)
            labels.append(sequence)

        return np.array(dataset), np.array(labels)

    def show_image(self, image):
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()