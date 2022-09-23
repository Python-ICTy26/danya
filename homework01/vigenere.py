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
    ciphertext = ""

    keyword = str(keyword * len(plaintext))[: len(plaintext)].lower()

    alf = [
        [
            chr(
                ord("a") + ord("a") + j + i - ord("z") - 1
                if ord("a") + j + i > ord("z")
                else ord("a") + j + i
            )
            for j in range(26)
        ]
        for i in range(26)
    ]

    for ich in range(len(plaintext)):
        ch = plaintext[ich]
        if ch.isalpha():
            chcode = alf[0].index(ch.lower())
            kch = keyword[ich]
            newch = alf[chcode][alf[0].index(kch)]
            if ch.isupper():
                ciphertext += newch.upper()
            else:
                ciphertext += newch
        else:
            ciphertext += ch

    return ciphertext


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
    plaintext = ""

    keyword = str(keyword * len(ciphertext))[: len(ciphertext)].lower()

    alf = [
        [
            chr(
                ord("a") + ord("a") + j + i - ord("z") - 1
                if ord("a") + j + i > ord("z")
                else ord("a") + j + i
            )
            for j in range(26)
        ]
        for i in range(26)
    ]

    for ich in range(len(ciphertext)):
        ch = ciphertext[ich]
        if ch.isalpha():
            kch = keyword[ich]
            kcode = alf[0].index(kch)
            lastch = ""
            for y in range(len(alf)):
                if alf[y][kcode] == ch.lower():
                    lastch = alf[0][y]
                    break
            if ch.isupper():
                plaintext += lastch.upper()
            else:
                plaintext += lastch
        else:
            plaintext += ch

    return plaintext
