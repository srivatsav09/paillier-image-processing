import random
import math
import time
import matplotlib.pyplot as plt

# Extended Euclidean Algorithm to find modular inverse
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

# Fast modular exponentiation
def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

# Generate large prime number
def generate_large_prime(bit_length):
    prime_candidate = random.getrandbits(bit_length)
    while not is_prime(prime_candidate):
        prime_candidate = random.getrandbits(bit_length)
    return prime_candidate

# Check if a number is prime
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# RSA Key Generation
def rsa_keygen(bit_length):
    p = generate_large_prime(bit_length)
    q = generate_large_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common choice for public exponent
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

# RSA Encryption and Decryption
def rsa_encrypt(plaintext, public_key):
    e, n = public_key
    return mod_pow(plaintext, e, n)

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    return mod_pow(ciphertext, d, n)

# Paillier Key Generation
def paillier_keygen(bit_length):
    p = generate_large_prime(bit_length)
    q = generate_large_prime(bit_length)
    n = p * q
    n_sq = n * n
    g = n + 1
    lambda_n = (p - 1) * (q - 1)
    mu = mod_inverse(lambda_n, n)
    return ((n, g), (lambda_n, mu))

# Paillier Encryption and Decryption
def paillier_encrypt(plaintext, public_key):
    n, g = public_key
    r = random.randint(1, n - 1)
    ciphertext = (pow(g, plaintext, n*n) * pow(r, n, n*n)) % (n*n)
    return ciphertext

def paillier_decrypt(ciphertext, private_key, public_key):
    n, _ = public_key
    lambda_n, mu = private_key
    plaintext = ((pow(ciphertext, lambda_n, n*n) - 1) // n * mu) % n
    return plaintext

# Perform multiple iterations and calculate average time for encryption
def calculate_encryption_time(algorithm, bit_length, plaintext):
    num_iterations = 10
    total_time = 0
    for _ in range(num_iterations):
        start_time = time.time()
        if algorithm == "RSA":
            public_key, _ = rsa_keygen(bit_length)
            rsa_encrypt(plaintext, public_key)
        elif algorithm == "Paillier":
            public_key, _ = paillier_keygen(bit_length)
            paillier_encrypt(plaintext, public_key)
        total_time += time.time() - start_time
    return total_time / num_iterations

# Testing RSA and Paillier encryption time
bit_length = 1024
plaintext = 1234567890

rsa_encryption_time = calculate_encryption_time("RSA", bit_length, plaintext)
paillier_encryption_time = calculate_encryption_time("Paillier", bit_length, plaintext)

# Plotting the results
labels = ['RSA', 'Paillier']
times = [rsa_encryption_time, paillier_encryption_time]

plt.bar(labels, times, color=['blue', 'green'])
plt.xlabel('Encryption Algorithm')
plt.ylabel('Time (seconds)')
plt.title('Encryption Time Comparison')
plt.show()
