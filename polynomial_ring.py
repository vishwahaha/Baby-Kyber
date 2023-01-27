from utils import *
from polynomial import Polynomial


class PolynomialRing:
    """
    This is a family of polynomials, every polynomial is of max degree 'n', and each coefficient is modulus 'q'
    """
    def __init__(self, q, n):
        self.q = q
        self.n = n
        self.element = Polynomial

    def decode(self, input_bytes, length=None):
        """
        Convert the input byte array to a polynomial, for further use
        """
        if length is None:
            length, check = divmod(8 * len(input_bytes), self.n)
            if check != 0:
                raise ValueError('Input bytes must be multiple of <poly degree>/8')
        else:
            if self.n * length != len(input_bytes) * 8:
                raise ValueError('Input bytes must be multiple of <poly degree>/8')
        coefficients = [0 for _ in range(self.n)]
        bit_list = bytes_to_bits(input_bytes)
        for i in range(self.n):
            coefficients[i] = sum(bit_list[i * length + j] << j for j in range(length))
        return self(coefficients)

    def __call__(self, coefficients):
        if isinstance(coefficients, int):
            return self.element(self, [coefficients])
        if not isinstance(coefficients, list):
            raise TypeError(
                f'Polynomials should be initialized from a list of integers of max length: d = {self.n}')
        return self.element(self, coefficients)

    def __repr__(self):
        return f'Polynomial ring R[x] over finite field of size {self.q} and modulus x^{self.n} + 1'
