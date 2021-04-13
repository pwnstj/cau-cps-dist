# 1. set p, q
# 2. n = p * q
# 3. phi(n)= (p-1)*(q-1)
# 4. find e: gcd((phi(n), e)) == 1, 1<e<phi(n)
# 5. find d: e * d mod phi(n) == 1, 1<d<phi(n)
# 6. encrypt
# 7. decrypt

from math import gcd    # gcd()  <-> import gcd -> math.gcd()


def setting(p: int, q: int):
    n = p * q
    phi_n = (p-1) * (q-1)
    e = find_e(phi_n)
    d = find_d(phi_n, e)
    print(n, e, d)
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


def encrypt(plain_text: str, pub_key: list):    # 0: n 1: e
    # c = p^e mod n
    plain_bytes = [ord(x) for x in plain_text]
    cipher_bytes = []
    print("plain_bytes:", plain_bytes)        # 10진법으로 표현된 평문

    for i in plain_bytes:
        cipher_bytes.append((i ** pub_key[1]) % pub_key[0])
    return cipher_bytes

# 실제 과제는 hex_text를 받음-> 파라미터 타입 str/ to_list함수 통해 리스트로 변경필요
def decrypt_by_rawcipher(cipher_list: list, pri_key):
    # p = c^d mod n
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

    plain_text = "plaintextisthis"

    cipher = encrypt(plain_text, pub_key)  # 10진법으로 표현된 암호문(리스트)
    dec_plain = decrypt_by_rawcipher(cipher, pri_key)
    print(dec_plain)

    hex_list = []                        # 16진법으로 표현된 암호문(리스트)
    for i in cipher:
        hex_list.append("{:02x}".format(i))
        # 문자열의 함수 split: 인자를 기준으로 문자열을 나눔  ex)0x5b -> 0, 5b
        # 나눠진 각 문자열은 배열 [-1]: 뒤에서 첫번째 원소
    hex_text = "0x" + "".join(hex_list)    # 16진법으로 표현된 암호문(문자열)
    # "y".join(x): 리스트 x의 각 원소 사이에 y를 삽입
    print(hex_text)
                        
