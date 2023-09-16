import random
import math

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Miller-Rabin primality test
    def check_composite(a, d, r, n):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    # Write n as 2^r * d + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        if check_composite(a, d, r, n):
            return False

    return True

def generate_random_prime(lower_limit, upper_limit):
    while True:
        candidate = random.randint(lower_limit, upper_limit)
        if is_prime(candidate):
            return candidate

def modular_inverse(a, m):
    # Calculate the modular multiplicative inverse of a modulo m
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("The modular inverse does not exist")
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)
    
def encryption_exponent(phi, n):
    e = None
    for i in range(2, phi):
        if math.gcd(i, phi) == 1 and math.gcd(i, n) == 1:
            e = i
            break
    if e is not None:
        return e
    raise Exception("there isn't any encryption exponent")

def rsa_generator():
    lower_limit = 2**100  
    upper_limit = 2**101  

    p = generate_random_prime(lower_limit, upper_limit)
    q = generate_random_prime(lower_limit, upper_limit)

    n = p * q

    phi = (p - 1) * (q - 1)

    e = encryption_exponent(phi, n)
    
    d = modular_inverse(e, phi)
    
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def test_rsa():
    public_key, private_key = rsa_generator()
    message = 123456789

    encrypted_message = pow(message, public_key[0], public_key[1])
    decrypted_message = pow(encrypted_message, private_key[0], private_key[1])

    # reverse test
    signature = pow(message, private_key[0], private_key[1])
    shown_signature = pow(signature, public_key[0], public_key[1])

    assert message == shown_signature
    assert message == decrypted_message

if __name__ == "__main__":
    test_rsa()