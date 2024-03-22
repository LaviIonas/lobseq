from read_binary_data import read_images, read_labels
from extract_files import extract_files

from random import choice
import random
import numpy as np

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

    def __calculate_bounds(self, digit, offset):
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
    
    def __determine_bounds(self, images, offset):
        bounds = []

        for img in images:
            bounds.append(self.__calculate_bounds(img, offset))

        return bounds
    
    """
    Can call this function for fun
    """
    def uniform_image_sequence(self, sequence, set):
        available_sets = ['train', 'test']

        if set not in available_sets:
            raise ValueError(f"Invalid set option '{set}'. Please choose from: {', '.join(available_sets)}.")

        images = []
        if set == 'train':
            for digit in sequence:
                img = self.X_train_raw[self.__select_random_train_label(digit)]
                images.append(img)
        else:
            for digit in sequence:
                img = self.X_test_raw[self.__select_random_test_label(digit)]
                images.append(img)
        
        return images
    
    def non_uniform_sequence(self, sequence, offset, canvas_inc):
        train_images = self.uniform_image_sequence(sequence, 'train')
        test_images = self.uniform_image_sequence(sequence, 'test')

        train_img_bounds = self.__determine_bounds(train_images, offset)
        test_img_bounds = self.__determine_bounds(train_images, offset)

        h , w = 28, 28
        canvas_h = h + canvas_inc
        canvas_w = w + canvas_inc

        noisy_train_images = []
        noisy_test_images = []

        for digit, (l_bound, r_bound) in zip(sequence, train_img_bounds):
            pass

        for digit, (l_bound, r_bound) in zip(sequence, test_img_bounds):
            pass
            
