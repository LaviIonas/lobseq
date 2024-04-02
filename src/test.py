from generate_mnist_sequence import lobseq

def main():
    path = "../data"
    lob = lobseq(path)
    X_train, y_train = lob.generate_random_database(3, 5, 1, 10, data_set='train')
    lob.show_image(X_train[0])
    print(y_train)

if __name__ == '__main__':
    main()