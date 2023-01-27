from baby_kyber import BabyKyber
from polynomial_ring import PolynomialRing
from matrix import Matrix

if __name__ == '__main__':
    kyber = BabyKyber(3329, 256, 2)
    pub, priv = kyber.keygen()
    (A, t) = pub
    print(A)
    print('------------')
    print(t)
    print('------------')
    print(priv)
    print('------------')
    message = 'test msg'
    for i in range(8):
        message += message
    message = message.encode()
    print('------------')
    print(message)
    u, v = kyber.encrypt(message, pub)
    print('------------')
    print(kyber.decrypt(u, v, priv))
