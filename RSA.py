#Trying to implement RSA
#If unsure refer to https://en.wikipedia.org/wiki/RSA_(cryptosystem)

def main():
    print("HELLO WORLD")
    first_prime, second_prime = generate_prime()
    public_key, private_key = generate_keys(first_prime, second_prime)
    print(public_key, private_key)
    message = input("Message to encrypt: ")
    print(message)
    encrypt_message(private_key, message)

def encrypt_message(private_key, message):
    #for i in message:
    encrypt_key, modulus = private_key
    print([ord(c) for c in message])
    message_ascii = [ord(c) for c in message]
    encrypted_message = []
    for i in message_ascii:
        #encrypted_message.append(math.pow(i,encrypt_key) % modulus)
        pass

def mod_exponential(num, power, mod):
    """
    >>> mod_exponential(3,4,5)
    1
    >>> mod_exponential(2007,2007,19)
    18
    >>> mod_exponential(93,4,100)
    1
    >>> mod_exponential(2013,1081,100)
    13
    """
    pow_remainder = {}
    pow_remainder[0] = 1
    #First find the inverse
    remainder = num % mod
    for x in range(1, power+1):
        if x == 1:
            remainder = num % mod
        else:
            remainder = remainder*num % mod
        pow_remainder[x] = remainder
        if remainder == 1 or remainder == (mod - 1):
            factor_power = x
            if remainder == mod - 1:
                remainder = -1
            exp_remainder = power % factor_power
            exp_quotient = math.floor(power/factor_power)
            if remainder == 1:
                mod_remainder = pow_remainder[exp_remainder]
            else:
                if exp_quotient % 2 == 0:
                    mod_remainder = pow_remainder[exp_remainder]
                else:
                    mod_remainder = -1 * pow_remainder[exp_remainder] + mod
            break
        if x == power:
            mod_remainder = remainder
    return mod_remainder

def mod_exponential_2(num, power, mod):
    """
    >>> mod_exponential_2(3,4,5)
    1
    >>> mod_exponential_2(2007,2007,19)
    18
    >>> mod_exponential(93,4,100)
    1
    >>> mod_exponential(2013,1081,100)
    13
    """
    #This one doesn't do anything special just calculates the mod of and exponential
    remainder = num % mod
    for x in range(power-1):
        remainder = num*remainder % mod
    return remainder


def generate_keys(first_prime, second_prime):
    modulus = first_prime * second_prime
    q = (first_prime - 1) * (second_prime - 1)
    while True:
        encrypt_key = random.randrange(2, q-1)
        if relative_coprime_check(encrypt_key, q) == True:
            break

    decrypt_key = 2
    for decrypt_key in range(2, encrypt_key-1):
        if decrypt_key * encrypt_key % q == 1:
            break
    print(first_prime, second_prime, q)
    print(modulus, encrypt_key, decrypt_key)
    public_key = [encrypt_key, modulus]
    private_key = [decrypt_key, modulus]
    return public_key, private_key

def relative_coprime_check(first, second):
    """
    >>> relative_coprime_check(5,4)
    True
    >>> relative_coprime_check(6,8)
    False
    >>> relative_coprime_check(27,21)
    False
    >>> relative_coprime_check(11,6)
    True
    >>> relative_coprime_check(523776, 267849)
    False
    """
    if first > second:
        size = second
    else:
        size = first
    for i in range(2,size):
        if first % i == 0 and second % i == 0:
            #These two numbers are not relatively coprime
            return False
    return True

def generate_prime():
    #Get 2 distinct prime numbers from the prime number list
    first_prime_index = random.randrange(0,len(prime_list)-1)
    second_prime_index = random.randrange(0,len(prime_list)-1)
    while first_prime_index == second_prime_index:
        second_prime_index = random.randrange(0,len(prime_list)-1)
    first_prime = prime_list[first_prime_index]
    second_prime = prime_list[second_prime_index]
    return first_prime, second_prime

if __name__ == "__main__":
    import doctest
    import random
    import math
    doctest.testmod()
    prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    main()


