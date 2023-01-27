#Baby Kyber
This is a scaled down implementation of NIST Finalist Post Quantum Cryptography algorithm, KYBER.  
###To generate public and private keys:  
`kb = BabyKyber(KYBER_Q, n, k)`  
`public_key, private_key = kb.keygen()`  
  
###To encrypt a message, which must be a bytes object:  
`cipher_u, cipher_v = kb.encrypt(message, public_key)`  
  
###To decrypt encrypted message:
`message = kb.decrypt(cipher_u, cipher_v, private_key)`