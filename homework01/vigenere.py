dictA = [chr(i) for i in range(65, 91)]
dicta = [chr(i) for i in range(97, 123)]
dict = dictA + dicta

def findIdx(c):
    return dict.index(c)

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    base = 52
    l = len(plaintext)
    lk = len(keyword)
    repeatN = l // lk
    remainder = l % lk
    fullKey = keyword * repeatN + keyword[: remainder]
    result = []
    for idx, val in enumerate(plaintext):
        key = findIdx(plaintext[idx]) + findIdx(fullKey[idx])
        result.append(dict[(key % base)])
    return ''.join(result)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    base = 52
    l = len(ciphertext)
    lk = len(keyword)
    repeatN = l // lk
    remainder = l % lk
    fullKey = keyword * repeatN + keyword[: remainder]
    result = []
    for idx, val in enumerate(ciphertext):
        key = findIdx(ciphertext[idx]) - findIdx(fullKey[idx]) + base
        result.append(dict[(key % base)])
    return ''.join(result)


if __name__ == '__main__':
    y = encrypt_vigenere('ATTACKATDAWN', 'LEMON')
    print(y)
    print(decrypt_vigenere(y, 'LEMON'))
