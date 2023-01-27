from utils import *


class Polynomial:
    def __init__(self, parent, coefficients):
        self.parent = parent
        self.coefficients = coefficients

    def is_zero(self):
        """
        :return: A boolean indicating whether polynomial is f(x) = 0
        """
        return all(coeff == 0 for coeff in self.coefficients)

    def is_constant(self):
        """
        :return: A boolean indicating whether polynomial is f(x) = k
        """
        return all(coeff == 0 for coeff in self.coefficients[1:])

    def add_mod_q(self, x, y):
        """
        add two coefficients modulo q
        """
        return (x + y) % self.parent.q

    def sub_mod_q(self, x, y):
        """
        sub two coefficients modulo q
        """
        tmp = x - y
        if tmp < 0:
            tmp += self.parent.q
        return tmp % self.parent.q

    def poly_multiplication(self, other):
        """
        Simple inefficient multiplication of two polynomials
        """
        n = self.parent.n
        a = self.coefficients
        b = other.coefficients
        new_coefficients = [0 for _ in range(n)]
        for i in range(n):
            for j in range(0, n - i):
                new_coefficients[i + j] += (a[i] * b[j])
        for j in range(1, n):
            for i in range(n - j, n):
                new_coefficients[i + j - n] -= (a[i] * b[j])
        return [c % self.parent.q for c in new_coefficients]

    def encode(self, length=None):
        """
        Encode this polynomial as bytes
        """
        if length is None:
            length = max(coeff.bit_length() for coeff in self.coefficients)
        bit_string = ''.join(format(coeff, f'0{length}b')[::-1] for coeff in self.coefficients)
        return bitstring_to_bytes(bit_string)

    def compress(self, d):
        """
        Compress each coefficient
        """
        compress_mod = 2 ** d
        compress_f = compress_mod / self.parent.q
        self.coefficients = [round_up(compress_f * coeff) % compress_mod for coeff in self.coefficients]
        return self

    def decompress(self, d):
        """
        Decompress each coefficient
        """
        decompress_f = self.parent.q / 2 ** d
        self.coefficients = [round_up(decompress_f * coeff) for coeff in self.coefficients]
        return self

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.coefficients == other.coefficients
        elif isinstance(other, int):
            if self.is_constant() and (other % self.parent.q) == self.coefficients[0]:
                return True
        return False

    def __neg__(self):
        """
        Returns -f(x)
        """
        neg_coefficients = [(-x % self.parent.q) for x in self.coefficients]
        return self.parent(neg_coefficients)

    def __add__(self, other):
        if isinstance(other, Polynomial):
            new_coefficients = [self.add_mod_q(x, y) for x, y in zip(self.coefficients, other.coefficients)]
        elif isinstance(other, int):
            new_coefficients = self.coefficients.copy()
            new_coefficients[0] = self.add_mod_q(new_coefficients[0], other)
        else:
            raise TypeError(f'Polynomials can only be added to each other')
        return self.parent(new_coefficients)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            new_coefficients = [self.sub_mod_q(x, y) for x, y in zip(self.coefficients, other.coefficients)]
        elif isinstance(other, int):
            new_coefficients = self.coefficients.copy()
            new_coefficients[0] = self.sub_mod_q(new_coefficients[0], other)
        else:
            raise TypeError(f'Polynomials can only be subtracted from each other')
        return self.parent(new_coefficients)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            new_coefficients = self.poly_multiplication(other)
        elif isinstance(other, int):
            new_coefficients = [(coeff * other) % self.parent.q for coeff in self.coefficients]
        else:
            raise TypeError(f'Polynomials can only be multiplied by each other, or scaled by integers')
        return self.parent(new_coefficients)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        self = self * other
        return self

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError(f'Exponentiation of a polynomial must be done using an integer.')
        if n < 0:
            raise ValueError(f'Negative powers are not supported for a Polynomial')
        f = self
        g = self.parent(1)
        while n > 0:
            if n % 2 == 1:
                g = g * f
            f = f * f
            n = n // 2
        return g

    def __getitem__(self, idx):
        return self.coefficients[idx]

    def __repr__(self):
        if self.is_zero():
            return '0'

        info = []
        for i, c in enumerate(self.coefficients):
            if c != 0:
                if i == 0:
                    info.append(f'{c}')
                elif i == 1:
                    if c == 1:
                        info.append('x')
                    else:
                        info.append(f'{c}*x')
                else:
                    if c == 1:
                        info.append(f'x^{i}')
                    else:
                        info.append(f'{c}*x^{i}')
        return ' + '.join(info)

    def __str__(self):
        return self.__repr__()
