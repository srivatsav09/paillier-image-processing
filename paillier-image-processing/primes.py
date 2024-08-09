# import random
# import sys

# def ipow(a, b, n):
# 	"""calculates (a**b) % n via binary exponentiation, yielding itermediate results as Rabin-Miller requires"""
# 	A = a = int(a % n)
# 	yield A
# 	t = 1
# 	while t <= b:
# 		t <<= 1

# 	t >>= 2
    
# 	while t:
# 		A = (A * A) % n
# 		if t & b:
# 			A = (A * a) % n
# 		yield A
# 		t >>= 1

# def rabin_miller_witness(test, possible):
# 	"""Using Rabin-Miller witness test, will return True if possible is
#        definitely not prime (composite), False if it may be prime."""    
# 	return 1 not in ipow(test, possible-1, possible)

# smallprimes = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,
#                47,53,59,61,67,71,73,79,83,89,97)

# def default_k(bits):
# 	return max(40, 2 * bits)

# def is_probably_prime(possible, k=None):
# 	if possible == 1:
# 		return True
# 	if k is None:
# 		k = default_k(possible.bit_length())
# 	for i in smallprimes:
# 		if possible == i:
# 			return True
# 		if possible % i == 0:
# 			return False
# 	for i in range(int(k)):
# 		test = random.randrange(2, possible - 1) | 1
# 		if rabin_miller_witness(test, possible):
# 			return False
# 	return True

# def generate_prime(bits, k=None):
# 	"""Will generate an integer of b bits that is probably prime 
#        (after k trials). Reasonably fast on current hardware for 
#        values of up to around 512 bits."""
# 	assert bits >= 8

# 	if k is None:
# 		k = default_k(bits)

# 	while True:
# 		possible = random.randrange(2 ** (bits-1) + 1, 2 ** bits) | 1
# 		if is_probably_prime(possible, k):
# 			return possible
	
import random
import sys

def jacobi_symbol(a, n):
    """Compute the Jacobi symbol (a/n), where n must be an odd positive integer."""
    assert n % 2 == 1 and n > 0
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

def mod_exp(base, exponent, modulus):
    """Compute (base^exponent) % modulus efficiently."""
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent //= 2
        base = (base * base) % modulus
    return result

def solovay_strassen_witness(test, possible):
    """Using Solovay-Strassen witness test, will return True if possible is
       definitely not prime (composite), False if it may be prime."""
    if mod_exp(test, (possible - 1) // 2, possible) == (jacobi_symbol(test, possible) % possible):
        return False
    else:
        return True

def is_probably_prime(possible, k=None):
    """Test if the given number is probably prime using Solovay-Strassen primality test."""
    if possible == 2:
        return True
    if possible % 2 == 0 or possible == 1:
        return False
    if k is None:
        k = 10  # Default number of iterations
    for i in range(k):
        test = random.randint(2, possible - 1)
        if solovay_strassen_witness(test, possible):
            return False
    return True

def generate_prime(bits, k=None):
    """Generate a probable prime number with the specified number of bits."""
    if k is None:
        k = 10  # Default number of iterations
    while True:
        possible = random.getrandbits(bits)
        if possible % 2 == 0:
            possible += 1
        if is_probably_prime(possible, k):
            return possible

# Example usage:
# prime = generate_prime(1024)  # Generate a 1024-bit prime number



