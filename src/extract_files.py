import os
import shutil

def extract_files(directory):
    # Check if the provided directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    # Check if the provided path is a directory
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    # List all files in the directory
    files = os.listdir(directory)

    # Check if all necessary files are present
    mnist_files = {
        'train_images': None,
        'train_labels': None,
        'test_images': None,
        'test_labels': None
    }

    for file in files:
        if file == 'train-images-idx3-ubyte':
            mnist_files['train_images'] = os.path.join(directory, file)
        elif file == 'train-labels-idx1-ubyte':
            mnist_files['train_labels'] = os.path.join(directory, file)
        elif file == 't10k-images-idx3-ubyte':
            mnist_files['test_images'] = os.path.join(directory, file)
        elif file == 't10k-labels-idx1-ubyte':
            mnist_files['test_labels'] = os.path.join(directory, file)

    # Check if all files are found
    if None in mnist_files.values():
        missing_files = [key for key, value in mnist_files.items() if value is None]
        raise FileNotFoundError(f"Missing files: {', '.join(missing_files)}")

    return mnist_files
