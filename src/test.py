from generate_mnist_sequence import lobseq

def main():
    path = "../data"
    lob = lobseq(path)
    # print(lob.X_train_raw.shape)

if __name__ == '__main__':
    main()