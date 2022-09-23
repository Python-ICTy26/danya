import string
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

    ciphertext = ""

    for ch in plaintext:
        if ch.isalpha():
            code = ord(ch) + shift
            if code > ord("Z" if ch.isupper() else "z"):
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += ch

    return ciphertext


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
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            code = ord(ch) - shift
            if code < ord("A" if ch.isupper() else "a"):
                code += 26
            plaintext += chr(code)
        else:
            plaintext += ch

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    for shift in range(26):
        plaintext = decrypt_caesar(ciphertext, shift)
        # or:
        # plaintext = ""
        # for ch in ciphertext:
        #     if ch.isalpha():
        #         code = ord(ch) - shift
        #         if code < ord('A' if ch.isupper() else 'a'):
        #             code += 26
        #         plaintext += chr(code)
        #     else:
        #         plaintext += ch

        if plaintext in dictionary:
            best_shift = shift
            break

    return best_shift
