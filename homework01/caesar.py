import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    tmp = [ord(c) for c in plaintext]
    A = []
    for i in tmp:
        if i in range(65, 91) or i in range(97, 123):
            if i > 90 - shift and i < 97:
                i = 64 - (90 - i)
            elif i > 122 - shift:
                i = 96 - (122 - i)
            i += shift
        A.append(i)
    result = [chr(c) for c in A]
    return ''.join(result)


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    tmp = [ord(c) for c in ciphertext]
    A = []
    for i in tmp:
        if i in range(65, 91) or i in range(97, 123):
            if i < 65 + shift:
                i = 90 + (i - 64)
            elif i > 90 and i < 97 + shift:
                i = 122 + (i - 96)
            i -= shift
        A.append(i)
    result = [chr(c) for c in A]
    return ''.join(result)


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift


if __name__ == '__main__':
    # x = encrypt_caesar('1@ABCDabcdUuWXYZwxyz')
    x = encrypt_caesar('pYThoN3.8')
    print(x)
    print(decrypt_caesar(x))
