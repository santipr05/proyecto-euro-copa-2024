import math

def isVapireNumber(n):
    n_digits = math.ceil(math.log10(n))
    digits = []
    permutation = []

    for i in range(n_digits):
        permutation.append(-1)

    if not n_digits % 2 == 0:
        return False

    def buildNumber(digits):
        result = 0;
        for d in digits:
            result = result * 10 + d

        return result

    def isVampire(digits):
        half = math.floor(len(digits)/2)
        a = buildNumber(digits[:half])
        b = buildNumber(digits[half:])
        if(a * b == n):
            return True

    def permutate(digit = 0):
        if not digit < n_digits:
            return isVampire(permutation)

        for i in range(n_digits):
            if i in permutation:
                continue
            permutation[digit] = digits[i]
            if permutate(digit + 1):
                return True
            permutation[digit] = -1

        return False

    for i in range(n_digits):
        digits.append(math.floor(n / math.pow(10, i)) % 10)

    return permutate()
