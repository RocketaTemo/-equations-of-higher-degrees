from decimal import Decimal


def get_coeff(massive, k, j, n):
    sum = massive[k - 1][j] ** 2

    for s in range(1, j + 1):
        if (j - s < 0) or (j + s > n):
            continue

        sum += 2 * ((0 - 1) ** s) * massive[k - 1][j - s] * massive[k - 1][j + s]

    return sum


def get_coeff_md_1(massive, k, j, n):
    sum = massive[k - 1][j] ** 2

    for s in range(1, j + 1):
        if (j - s < 0) or (j + s > n):
            continue
        sum += ((0 - 1) ** s) * massive[k - 1][j - s] * massive[k - 1][j + s]

    return sum


def get_coeff_md_2(massive, k, j, n):
    sum = massive[k - 1][j]

    for s in range(1, j + 1):
        if (j - s < 0) or (j + s > n):
            continue
        sum += 2 * ((0 - 1) ** s) * massive[k - 1][j - s] * massive[k - 1][j + s]

    return sum


def get_coeff_md_3(massive, k, j, n):
    sum = 0

    for s in range(1, j + 1):
        if (j - s < 0) or (j + s > n):
            continue

        sum += 2 * ((0 - 1) ** s) * massive[k - 1][j - s] * massive[k - 1][j + s]

    return sum


def get_coeff_md_4(massive, k, j, n):
    sum = massive[k - 1][j]

    for s in range(1, j + 1):
        if (j - s < 0) or (j + s > n):
            continue

        sum += 2 * massive[k - 1][j - s] * massive[k - 1][j + s]

    return sum


def stop(massive, g, n, h):
    if g < 4:
        return False
    for j in range(0, n):
        if massive[g][j] < 0 or massive[g - 1][j] < 0:
            continue

        if r_f(massive[g][j], h) != r_f(massive[g - 1][j] ** 2, h):
            return False
    return True


def r_f(num, h):
    p = 0
    if num == 0:
        return 0

    while abs(num) >= 10:
        p += 1
        num = num / 10
    while abs(num) < 1:
        p -= 1
        num = num * 10

    return round(num, h) * Decimal(10 ** p)


def get_orient(massive, x, n):
    sum = 0

    for coeff in massive[0]:
        sum += coeff * x ** n
        n -= 1

    if round(r_f(sum, 1)) == Decimal(0):
        return True
    else:
        return False


def get_x_md_1(coeff, g, l, n, h):
    a = coeff[g][l]
    b = coeff[g][l - 1]

    x = r_f((a / b) ** Decimal(1 / (2 * g)), h)
    if type(x) == complex:
        x = x.real

    if get_orient(coeff, x, n):
        return r_f(x, h)
    else:
        return r_f(-x, h)


def get_x_md_2(coeff, g, l, n, h):
    a = coeff[g][l]
    b = coeff[g][l - 1]

    x = r_f((a / b), h)
    if type(x) == complex:
        x = x.real

    if get_orient(coeff, x, n):
        return r_f(x, h)
    else:
        return r_f(-x, h)
