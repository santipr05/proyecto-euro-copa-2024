import math

IS_DEV = True

def printDebugInfo(message):
    if IS_DEV:
        print(f"[Debug]: {message}")

def isPerfectNumber(n):
  if n <= 1:
    return False

  divider_sum = 1
  for divisor in range(2, n):
    if n % divisor == 0:
      divider_sum += divisor

  return n == divider_sum

def inputInt(propmt, errorMsg = "Ingrese un numero."):
    result = 0
    valid = False

    while not valid:
        try:
            result = int(input(propmt))
            valid = True
        except ValueError:
            print(errorMsg)

    return result

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
