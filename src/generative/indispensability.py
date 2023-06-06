from math import sqrt


def prime_factors(n: int) -> list[int]:
    """Returns the prime factors of a number.

    Parameters
    ----------
    n : int
        The number to factorize.

    Returns
    -------
    list[int]
        The prime factors of the number.
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)

    return factors


def time_signature_factors(
    nominator: int, denominator: int, metric_level: int = 16
) -> list[int]:
    """Returns the prime factors of a time signature.

    Parameters
    ----------
    nominator : int
        The nominator of the time signature.
    denominator : int
        The denominator of the time signature.

    Returns
    -------
    list[int]
        The prime factors of the time signature.
    """
    subdivisions = metric_level // denominator

    return prime_factors(nominator) + prime_factors(subdivisions)


def product_top(z: int, factors: list[int]):
    mult = 1

    for j in range(1, z + 1):
        mult *= factors[j]

    return mult


def product_bottom(z: int, r: int, factors: list[int]):
    mult = 1

    for k in range(r + 1):
        mult *= factors[z + 1 - k]

    return mult


def pulse_weights(
    nominator: int, denominator: int, metric_level: int = 16
) -> list[float]:
    primes = time_signature_factors(nominator, denominator, metric_level)
    pulses = metric_level // denominator * nominator
    primes = [1] + primes + [1]

    max_value = pulses - 1
    indispensabilities = [
        (indispensability(pulse, primes) / max_value) * 0.3 + 0.7
        for pulse in range(1, pulses + 1)
    ]
    return indispensabilities


def indispensability(pulse: int, primes: list[int]) -> int:
    z = len(primes) - 2
    top = product_top(z, primes)
    sum = 0
    for r in range(z):
        bot = product_bottom(z, r, primes)

        mult = 1
        for i in range(z - r):
            mult *= primes[i]

        modulo = primes[z - r]
        temp = ((pulse - 2) % top) / bot
        temp = int(1 + temp)
        temp = temp % modulo
        temp = 1 + temp

        basic = basic_indispensability(temp, primes[z - r])

        sum += mult * basic

    return sum


def w_func(x: int) -> int:
    if x == 0:
        return 0

    return 1


def basic_indispensability(pulse: int, prime: int) -> int:
    """Returns the basic indispensability of a pulse.

    Parameters
    ----------
    pulse : int
        The pulse to calculate the basic indispensability of.
    prime : int
        The prime to calculate the basic indispensability of.

    Returns
    -------
    int
        The basic indispensability of the pulse.
    """
    # if prime == 2:
    #     return prime - pulse

    # if pulse == prime - 1:
    #     return prime // 4

    # factors = prime_factors(prime - 1)[::-1]
    # factors = [1] + factors + [1]
    # q = indispensability(pulse - pulse // prime, factors)
    # return int(q + 2 * sqrt((q + 1) / prime))
    if prime <= 3:
        return (prime + pulse - 2) % prime

    new_pulse = pulse - 1 + w_func(prime - pulse)
    factors = prime_factors(prime - 1)[::-1]
    factors = [1] + factors + [1]
    q = indispensability(new_pulse, factors)

    return (q + w_func(int(q / (prime // 4)))) * w_func(prime - pulse - 1) + (
        prime // 4
    ) * (1 - w_func(prime - pulse - 1))
