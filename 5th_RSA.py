
from math import gcd

p = 11
q = 11113
n = p * q
phi_n = (p-1) * (q-1)

e = 2

while gcd(phi_n, e) != 1:
    e += 1
    print(e)

d = 0
mod = 0
while 1:
    d += 1
    mod = (e * d) % phi_n
    if mod == 1:
        break

# 암호화, c=m^e mod n

plain = "aleopwafkeofp13fkowe"
plain_list = [ord(x) for x in plain]  # ord(x): x를 아스키코드로 변환
# for  x in plain; plain_list.append(ord(x)); 와 동일

cipher = []
for i in plain_list:
    x = (i ** e) % n
    cipher.append(int(x))

# 복호화, m = c^d mod n

decrypted = []
for i in cipher:
    x = (i ** d) % n
    decrypted.append(int(x))

print("plain text:", plain_list)
print("cipher text: ", cipher)
print("decrypted text: ", decrypted)

print([chr(x) for x in decrypted])
decrypted_text = "".join([chr(x) for x in decrypted])
print(decrypted_text)
# chr(x) 아스키코드 x를 문자로 변환
# join: 문자열로 변환
