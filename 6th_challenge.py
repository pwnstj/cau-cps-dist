
from math import gcd
import random


def eratosthenes(max_num: int):            # 1~max_num의 소수를 찾는 함수
    sieve = [1 for i in range(max_num+1)]
    primes_low = []
    primes_high = []
    
    for i in range(2, int(max_num ** 0.5) + 1):
        if sieve[i]:
            for j in range(2 * i, max_num+1, i):
                sieve[j] = 0
    for i in range(2, max_num+1):
        if sieve[i] and i>=100:
            if i<500:
                primes_low.append(i)
            else:
                primes_high.append(i)

    return primes_low, primes_high
                
def setting(p: int, q: int):
    n = p * q
    phi_n = (p-1) * (q-1)
    e = find_e(phi_n)
    d = find_d(phi_n, e)
    print("p: %d, q: %d, n: %d, e: %d, d: %d" % (p, q, n, e, d))
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
    tok_num = 8
    for i in range(2, len(hex_text), tok_num):
        temp = []
        for j in range(tok_num):
            temp.append(hex_text[i+j])
        cipher_list.append(int("".join(temp), 16))    #int(str, str이 몇진수를 나타내는지)
    return cipher_list


def decrypt_hexcipher(hex_text: str, pri_key):
    # p = c^d mod n
    cipher_list = to_list(hex_text)
    print(cipher_list)
    plain_bytes = []
    for i in cipher_list:
        plain_bytes.append((i ** pri_key[1]) % pri_key[0])
    print(plain_bytes)
    plain_text = "".join([chr(x) for x in plain_bytes])
    return plain_text


if __name__ == "__main__": # 메인함수
    primes_low, primes_high = eratosthenes(1000)
    for i in primes_low:
        for j in primes_high:
            flag = 0
            p = i
            q = j
            n, e, d = setting(p, q)

            pub_key = [n, e]
            pri_key = [n, d]

            hex_text = '''0x0003b971000114f60001caef0002e6c900043e9e00043e9e0003a6210004702100047bf40003b101000352ce00030c960003a62100043e9e00043e9e0003a6210002e6c90001bdf8000352ce0003142d0002e6c9000114f60001caef00047bf40003b1010002c0730003b101000355f6000355f6'''
        
            dec_plain = decrypt_hexcipher(hex_text, pri_key)
            try:
                print("복호화 결과: %s" % dec_plain)
            except:
                pass
            
            for k in dec_plain:
                if k > '~':
                    flag = 1
            if flag == 0:
                break
        if flag == 0:
                print("복호화 성공")
                break
    