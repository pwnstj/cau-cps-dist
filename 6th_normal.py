
from math import gcd


def setting(p: int, q: int):
    n = p * q
    phi_n = (p-1) * (q-1)
    e = find_e(phi_n)
    d = find_d(phi_n, e)
    print("n: %d, e: %d, d: %d" % (n, e, d))
    return n, e, d


def find_e(phi_n: int):
    e = 0
    for i in range(2, phi_n):
        if gcd(phi_n, i) == 1:
            e = i
            break
    return e


def find_d(phi_n: int, e: int):
    d = 0
    for i in range(2, phi_n):
        if (e * i) % phi_n == 1:
            d = i
            break
    return d


def to_list(hex_text: str):        # 16진수로 이루어진 문자열을 10진수 리스트로 변환하는 함수
    cipher_list = []
    tok_num = 2
    for i in range(2, len(hex_text), tok_num):
        temp = []
        for j in range(tok_num):
            temp.append(hex_text[i+j])
        cipher_list.append(int("".join(temp), 16))
        print(temp)
    return cipher_list


def decrypt_hexcipher(hex_text: str, pri_key):
    # p = c^d mod n
    cipher_list = to_list(hex_text)

    plain_bytes = []
    for i in cipher_list:
        plain_bytes.append((i ** pri_key[1]) % pri_key[0])

    plain_text = "".join([chr(x) for x in plain_bytes])
    return plain_text


if __name__ == "__main__":     # 메인함수
    p = 11
    q = 13
    n, e, d = setting(p, q)

    pub_key = [n, e]
    pri_key = [n, d]

    hex_text = "0x4d765050762d2162592d1512043e813e6e6e"

    dec_plain = decrypt_hexcipher(hex_text, pri_key)
    print("복호화 결과: %s" % dec_plain)
