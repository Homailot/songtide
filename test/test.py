from src.generative import euclidean, fractal


def test():
    print(euclidean.euclidean_rhythm_simple(13, 5, 1))
    print(euclidean.euclidean_rhythm(13, 5, 1))
    print(euclidean.euclidean_rhythm(13, 5, 2))
    print(euclidean.euclidean_rhythm(13, 5, 3))
    print(euclidean.euclidean_rhythm(13, 5, 4))

    for i in range(0, 10):
        print(fractal.morse_thue_value(i, 2, 1))

    print(-4 // 3)