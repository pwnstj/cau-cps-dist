from math import gcd
import random


class RSA:
    def __init__(self):
        __prime_list = self.primes_in_range(10, 99)  # 각 객체의 p, q는 2자리 소수
        __p = random.choice(__prime_list)    # choice(list): list에서 랜덤하게 하나를 뽑음
        __prime_list.remove(__p)             # p, q 중복 방지
        __q = random.choice(__prime_list)

        n, e, d = self.init_setting(__p, __q)
        self.pub_key = [n, e]
        self.pri_key = [n, d]

    def init_setting(self, p: int, q: int):
        n = p * q
        phi_n = (p-1) * (q-1)
        e = self.find_e(phi_n)
        d = self.find_d(phi_n, e)

        return n, e, d

    @staticmethod
    def find_e(phi_n: int):
        temp_e = 0
        for i in range(2, phi_n):
            if gcd(phi_n, i) == 1:
                temp_e = i
                break
        return temp_e

    @staticmethod
    def find_d(phi_n: int, e: int):
        temp_d = 1
        for i in range(phi_n):
            if (e * i) % phi_n == 1:
                temp_d = i
                break
        return temp_d

    @staticmethod
    def primes_in_range(x: int, y: int):  # 에라토스테네스의 체 활용
        prime = [True] * y
        for i in range(2, int(y ** 0.5) + 1):
            if prime[i]:
                for j in range(i+i, y, i):
                    prime[j] = False
        prime_list = [i for i in range(2, y) if prime[i]]

        return [i for i in prime_list if i >= x]

    @staticmethod
    def encrypt(plain_text: str, key: list):
        plain_bytes = [ord(x) for x in plain_text]
        cipher_bytes = []
        for i in plain_bytes:
            cipher_bytes.append((i ** key[1]) % key[0])

        cipher_hex = []  # 메시지가 str타입이므로 암호문 전송하기 위해서는 str로 변환하는 과정이 필요
        for i in cipher_bytes:
            tmp_hex = "{:08x}". format(i)
            cipher_hex.append(tmp_hex)
        cipher_text = "0x" + "".join(cipher_hex)

        return cipher_text

    @staticmethod
    def decrypt(cipher_text: str, key: list):
        cipher_tmp = cipher_text.split("x")[-1]
        tok_length = 8
        cipher_bytes  = [int(cipher_tmp[x: x+tok_length], 16) for x in range(0, len(cipher_tmp), tok_length)]

        plain_bytes = []
        for i in cipher_bytes:
            plain_bytes.append((int(i) ** key[1]) % key[0])

        dec_text = "".join([chr(x) for x in plain_bytes])
        return dec_text


class Person:    # 클래스: 함수, 변수의 집합
    def __init__(self, name: str):    # 클래스 초기화 함수(메소드), 클래스 객체 생성시 실행
        # instance method: self를 첫번째 인자로 받음
        # staticmethod: 객체내부 상태를 변화시키지 않음
        self.name = name    # 객체변수
        self.rsa = RSA()
        self.communication = Communication()

        self.nonce = str(random.randint(0, 10000))
        self.target_key = []  # 상대방의 개인키를 담는 리스트
        self.__msg_history = []  # 주고받은 메세지를 저장하는 리스트
        # 클래스 안 __변수: private변수로, 외부접근 차단 /e.g. 메인함수에서 print(bob.__msg_history)와 같이 접근할 수 없음

    def recv_msg(self, msg: str):    # 상대방이 보낸 메시지를 msghistory에 추가
        self.__msg_history.append(msg)

    def recv_key(self, key: list):    # 상대방이 보낸 키를 객체변수에 저장
        self.target_key = key

    def get_latest_msg(self):
        return self.__msg_history[-1]  # 가장 끝에 있는 요소 출력


class Communication:
    @staticmethod
    def send_msg(target: Person, msg: str):
        target.recv_msg(msg)

    @staticmethod
    def send_key(target: Person, key: list):
        target.recv_key(key)


if __name__ == '__main__':
    alice = Person("alice")    # Person 클래스 형태의 객체 생성
    bob = Person("bob")

    say_hi = "Hi! I'm alice"
    alice.communication.send_msg(bob, say_hi)  # bob에게 문자열 say_hi를 전송
    print(bob.get_latest_msg())

    bob.communication.send_msg(alice, bob.nonce)  # alice에게 bob의 nonce를 전송
    print("bob의 nonce: ", bob.nonce)
    print("alice가 받은 nonce: ", alice.get_latest_msg())

    # bob이 보낸 nonce를 alice의 개인키로 암호화
    alice.communication.send_msg(bob, alice.rsa.encrypt(alice.get_latest_msg(), alice.rsa.pri_key))
    print("alice의 개인키로 암호화된 bob의 nonce: ", bob.get_latest_msg())
    # alice의 공개키 요청
    bob.communication.send_msg(alice, "send your public key")
    # alice의 공개키 전송
    alice.communication.send_key(bob, alice.rsa.pub_key)
    print("alice의 공개키: ", bob.target_key)

    if bob.nonce == bob.rsa.decrypt(bob.get_latest_msg(), bob.target_key):
        say_hello = "Hello! I'm Bob"
        bob.communication.send_msg(alice, bob.rsa.encrypt(say_hello, bob.target_key))
        print(say_hello)
    else:
        print("is hacked")

    print("check: ", alice.rsa.decrypt(alice.get_latest_msg(), alice.rsa.pri_key))
