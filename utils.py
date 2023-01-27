def bytes_to_bits(input_bytes):
    """
    Convert bytes to a bit array(little endian format)
    :return: list of bits
    """
    # [::-1] is the fastest way to reverse a string
    bit_string = ''.join(format(byte, '08b')[::-1] for byte in input_bytes)
    return list(map(int, list(bit_string)))


def bitstring_to_bytes(bit_s):
    """
    Converts a string of bits to bytes(stored in little endian)
    :param bit_s: string of input bits
    :return: bytes
    """
    return bytes([int(bit_s[i:i + 8][::-1], 2) for i in range(0, len(bit_s), 8)])


def round_up(x):
    """
    Round x.5 to x+1
    """
    return round(x + 0.000001)
