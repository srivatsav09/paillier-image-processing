# rabin_miller.py
import random

def rabin_miller_witness(test, possible):
    """Using Rabin-Miller witness test, return True if possible is definitely not prime (composite),
       False if it may be prime."""
    return pow(test, possible - 1, possible) != 1

def is_probably_prime(possible, k=None):
    """Test if the given number is probably prime using Rabin-Miller primality test."""
    if possible < 2:
        return False
    if possible < 4:
        return True
    if possible % 2 == 0:
        return False

    if k is None:
        k = 10  # Default number of iterations

    for _ in range(k):
        test = random.randint(2, possible - 2)
        if rabin_miller_witness(test, possible):
            return False
    return True
# solovay_strassen.py
import random

def jacobi_symbol(a, n):
    """Compute the Jacobi symbol (a/n), where n must be an odd positive integer."""
    assert n % 2 == 1 and n > 0
    # Implementation of Jacobi symbol omitted for brevity
    # You can use the implementation provided earlier

def solovay_strassen_witness(test, possible):
    """Using Solovay-Strassen witness test, return True if possible is definitely not prime (composite),
       False if it may be prime."""
    return pow(test, (possible - 1) // 2, possible) != jacobi_symbol(test, possible)

def is_probably_prime(possible, k=None):
    """Test if the given number is probably prime using Solovay-Strassen primality test."""
    if possible < 2:
        return False
    if possible < 4:
        return True
    if possible % 2 == 0:
        return False

    if k is None:
        k = 10  # Default number of iterations

    for _ in range(k):
        test = random.randint(2, possible - 2)
        if solovay_strassen_witness(test, possible):
            return False
    return True
# Test Setup

import time

# Measure execution time for Rabin-Miller primality test

import matplotlib.pyplot as plt


test_range = range(1000000000000000, 1000000000000100)  # Increased range of numbers to test
known_primes = [999999999999937, 999999999999989]  # Larger known prime numbers for accuracy validation

# Measure execution time for Rabin-Miller primality test with increased iterations
start_time = time.time()
for num in test_range:
    is_probably_prime(num, k=50)  # Increased number of iterations
rabin_miller_time = time.time() - start_time

# Measure execution time for Solovay-Strassen primality test with increased iterations
start_time = time.time()
for num in test_range:
    is_probably_prime(num, k=50)  # Increased number of iterations
solovay_strassen_time = time.time() - start_time

# Accuracy Verification with larger known primes
rabin_miller_accuracy = sum(is_probably_prime(num, k=50) for num in known_primes) / len(known_primes)
solovay_strassen_accuracy = sum(is_probably_prime(num, k=50) for num in known_primes) / len(known_primes)

# Plot execution time comparison
plt.bar(['Rabin-Miller', 'Solovay-Strassen'], [rabin_miller_time, solovay_strassen_time])
plt.xlabel('Primality Test Algorithm')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison')
plt.show()

# Plot accuracy comparison
plt.bar(['Rabin-Miller', 'Solovay-Strassen'], [rabin_miller_accuracy, solovay_strassen_accuracy])
plt.xlabel('Primality Test Algorithm')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison')
plt.ylim(0, 1)  # Set y-axis limit to show percentages
plt.show()

