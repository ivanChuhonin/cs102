import string

dictA = [chr(i) for i in range(65, 91)]
dict = list(string.ascii_uppercase)# + dicta

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

    base = len(dict)
    Ukeyword = keyword.upper()
    Uplaintext = plaintext.upper()
    l = len(plaintext)
    lk = len(Ukeyword)
    repeatN = l // lk
    remainder = l % lk
    fullKey = Ukeyword * repeatN + Ukeyword[: remainder]
    result = []
    for idx, val in enumerate(Uplaintext):
        if plaintext[idx] in string.ascii_letters:
            key = findIdx(Uplaintext[idx]) + findIdx(fullKey[idx])
            if plaintext[idx].isupper():
                result.append(dict[(key % base)])
            else:
                result.append(dict[(key % base)].lower())
        else:
            result.append(plaintext[idx])
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
    base = len(dict)
    Ukeyword = keyword.upper()
    Uciphertext = ciphertext.upper()
    l = len(ciphertext)
    lk = len(keyword)
    repeatN = l // lk
    remainder = l % lk
    fullKey = Ukeyword * repeatN + Ukeyword[: remainder]
    result = []
    for idx, val in enumerate(Uciphertext):
        if ciphertext[idx] in string.ascii_letters:
            key = findIdx(Uciphertext[idx]) - findIdx(fullKey[idx]) + base
            if ciphertext[idx].isupper():
                result.append(dict[(key % base)])
            else:
                result.append(dict[(key % base)].lower())
        else:
            result.append(ciphertext[idx])
    return ''.join(result)


if __name__ == '__main__':
    y = encrypt_vigenere('ATTACKATDAWN', 'LEMON')
    print(y)
    print(decrypt_vigenere(y, 'LEMON'))
