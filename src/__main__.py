from generative import euclidean


def main():
    print(euclidean.euclidean_rhythm_simple(13, 5, 1))
    print(euclidean.euclidean_rhythm(13, 5, 1))
    print(euclidean.euclidean_rhythm(13, 5, 2))
    print(euclidean.euclidean_rhythm(13, 5, 3))
    print(euclidean.euclidean_rhythm(13, 5, 4))


if __name__ == "__main__":
    main()
