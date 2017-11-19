#Trying to implement RSA
#If unsure refer to https://en.wikipedia.org/wiki/RSA_(cryptosystem)

def main():
    print("Type help for instructions")
    public_key = [None]
    private_key = [None]
    while True:
        public_key, private_key = interface(public_key, private_key)
    first_prime, second_prime = generate_prime()
    public_key, private_key = generate_keys(first_prime, second_prime)
    print(public_key, private_key)
    message = input("Message to encrypt: ")
    print(message)
    print([ord(c) for c in message])
    message_ascii = [ord(c) for c in message]
    encrypted_message = encrypt_message(private_key, message_ascii)
    print(encrypted_message)
    decrypted_message = decrypt_message(public_key, encrypted_message)
    print(decrypted_message)
    print_ascii(decrypted_message)

def load_private_key():
    try:
        with open("private_key") as f:
            private_key = f.read()
        f.close()
        str_list = private_key.split()
        new_private_key = []
        for i in range(len(str_list)):
            key = int(str_list[i])
            new_private_key.append(key)
        return(new_private_key)
    except:
        print("Cannot find private_key")
        return([None])

def load_public_key():
    try:
        with open("public_key") as f:
            public_key = f.read()
        f.close()
        str_list = public_key.split()
        new_public_key = []
        for i in range(len(str_list)):
            key = int(str_list[i])
            new_public_key.append(key)
        return(new_public_key)
    except:
        print("Cannot find public_key")
        return([None])

def save_keys(public_key, private_key):
    valid_public_key = True
    valid_private_key = True
    for i in range(len(public_key)):
        try:
            if public_key[i] < 2:
                print("Not valid public key: ", public_key)
                valid_public_key = False
        except:
            print("Not valid public key: ", public_key)
            valid_public_key = False
    if len(public_key) != 2 or len(private_key) != 2:
        valid_public_key = False
        valid_private_key = False
    for i in range(len(private_key)):
        try:
            if private_key[i] < 2:
                print("Not valid private key: ", private_key)
                valid_private_key = False
        except:
            print("Not valid private key: ", private_key)
            valid_private_key = False
    if valid_public_key == True and valid_private_key == True:
        public_key_str = str(public_key[0]) + " " + str(public_key[1])
        with open("public_key",'w') as f:
            f.write(public_key_str)
        f.close()

        private_key_str = str(private_key[0]) + " " + str(private_key[1])
        with open("private_key",'w') as f:
            f.write(private_key_str)
        f.close()

def print_keys(public_key, private_key):
    print("Public key is:", public_key)
    print("Private key is:", private_key)

def generate_key_pair():
    first_prime, second_prime = generate_prime()
    public_key, private_key = generate_keys(first_prime, second_prime)
    print("Public key is:", public_key)
    print("Private key is:", private_key)
    return public_key, private_key

def help():
    print(
"""\tInstruction\t\tDescription
\tgenerate keys\t\tgenerate a public and private key pair
\tprint keys\t\tprint current key pair
\tsave keys\t\tsave the generate key into file in same directory
\tload public key\t\tread public key from file
\tload private key\t\tread private key from file
\tencrypt message\t\tenter message to be encrypted by private key
\tdecrypt message\t\tenter message to be decrypted by public key
\tInstruction\t\tDescription
\texit\t\t\texit program""")

def interface(public_key, private_key):
    function = input("> ").lower()
    if function == "help":
        help()
    elif function == "generate keys":
        public_key, private_key = generate_key_pair()
        return public_key, private_key
    elif function == "print keys":
        print_keys(public_key, private_key)
    elif function == "save keys":
        save_keys(public_key, private_key)
    elif function == "load public key":
        public_key = load_public_key()
    elif function == "load private key":
        private_key = load_private_key()
    elif function == "encrypt message":
        pass
    elif function == "decrypt message":
        pass
    elif function == "exit":
        sys.exit()
    else:
        print(function, "command not found")
    return public_key, private_key

def print_ascii(message):
    for i in message:
        print(chr(i), end = '')
    print("")

def decrypt_message(public_key, message):
    decrypt_key, modulus = public_key
    decrypted_message = []
    for i in message:
        decrypted_message.append(mod_exponential(i,decrypt_key,modulus))
    return decrypted_message

#Encrypt_message takes the private_key tuple and the message already converted into ascii
def encrypt_message(private_key, message):
    encrypt_key, modulus = private_key
    encrypted_message = []
    for i in message:
        encrypted_message.append(mod_exponential(i,encrypt_key,modulus))
    return encrypted_message

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
    >>> mod_exponential(2015,1082,11)
    4
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
    >>> mod_exponential(2015,1082,11)
    4
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
    import sys
    doctest.testmod()
    prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    main()


