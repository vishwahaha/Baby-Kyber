import random
from polynomial_ring import PolynomialRing
from matrix import Matrix


class BabyKyber:
    def __init__(self, kyber_q, n, k):
        """
        :param kyber_q: Q defines the max and min values of coefficients of polynomials (3329 in kyber)
        :param n: Degree of polynomial (256 in kyber)
        :param k: dimension of matrices used
        """
        if k not in (2, 3, 4):
            raise ValueError('Value of matrix size must be 2, 3 or 4')
        self.k = k
        self.R = PolynomialRing(kyber_q, n)
        self.M = Matrix(self.R)

    def keygen(self):
        """
        :return: A public and a private key used for KYBER encryption and decryption respectively
        """
        # Generate private key, s
        s_list = []
        for i in range(self.k):
            s_list.append(self.rand_small_polynomial())
        s = self.M(s_list).transpose()

        # Generate part of public key, A
        A_list = []
        for i in range(self.k):
            A_sublist = []
            for j in range(self.k):
                A_sublist.append(self.rand_polynomial_modq())
            A_list.append(A_sublist)
        A = self.M(A_list)

        # Generate error vector, e
        e_list = []
        for i in range(self.k):
            e_list.append(self.rand_small_polynomial())
        e = self.M(e_list).transpose()

        # Calculate part of public key, t = As + e
        t = A @ s + e
        return (A, t), s

    def encrypt(self, message, public_key):
        """
        :param message: message to encrypt as bytes
        :param public_key: KYBER public key which will be used to encrypt the message
        :return: encrypted message
        """
        A, t = public_key
        poly_m = self.R.decode(message).decompress(1)
        # Generate randomizer vector
        r_list = []
        for i in range(self.k):
            r_list.append(self.rand_small_polynomial())
        r = self.M(r_list).transpose()

        # Generate error vector
        e_1_list = []
        for i in range(self.k):
            e_1_list.append(self.rand_small_polynomial())
        e_1 = self.M(e_1_list).transpose()

        # Generate error polynomial
        e_2 = self.rand_small_polynomial()

        # Calculate u & v
        u = A.transpose() @ r + e_1
        v = (t.transpose() @ r)[0][0] + e_2 - poly_m
        return u, v

    def decrypt(self, cipher_u, cipher_v, private_key):
        """
        :param cipher_u: cipher text u: A.transpose() @ r + e_1
        :param cipher_v: cipher text v: t.transpose() @ r + e_2 - m
        :param private_key: KYBER private key (s)
        :return: decrypted message in bytes
        """
        m_n = cipher_v - (private_key.transpose() @ cipher_u)[0][0]
        m_n_reduced = m_n.compress(1)
        return m_n_reduced.encode()

    def rand_small_polynomial(self):
        """
        Generate a random 'small' polynomial
        """
        SMALL_NUMBER_LIMIT = 1
        coefficients = []
        for i in range(self.R.n):
            coefficients.append(random.randint(-SMALL_NUMBER_LIMIT, SMALL_NUMBER_LIMIT))
        return self.R(coefficients)

    def rand_polynomial_modq(self):
        """
        Generate a polynomial with random coefficients modulus KYBER_Q
        """
        coefficients = []
        for i in range(self.R.n):
            coefficients.append(random.randint(1 - self.R.q, self.R.q-1))
        return self.R(coefficients)
