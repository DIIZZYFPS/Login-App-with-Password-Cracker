import itertools
import string
import time

class Crack:

    def brute_force(self, password):
        chars = string.ascii_lowercase + string.digits
        start_time = time.time()  
        for length in range(1, len(password) + 1):
            for guess in itertools.product(chars, repeat=length):
                guess = ''.join(guess)
                if guess == password:
                    end_time = time.time()  
                    elapsed_time = end_time - start_time
                    return guess, elapsed_time
                if time.time() - start_time > 30:
                    return None, 30
        end_time = time.time()  
        elapsed_time = end_time - start_time
        return None, elapsed_time
    
    def dictionary_attack(self, password, dictionary='words.txt'):
        start_time = time.time()
        try:
            with open(dictionary, 'r') as file:
                words = [line.strip() for line in file]

                # Check for exact matches
                for guess in words:
                    if guess == password:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        return guess, elapsed_time
                    if time.time() - start_time > 90:
                        return None, 30
                
                # Check for combinations of words
                for length in range(2, 4):  
                    for guess_tuple in itertools.product(words, repeat=length):
                        guess = ''.join(guess_tuple)
                        if guess == password:
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            return guess, elapsed_time
                        if time.time() - start_time > 90:
                            return None, 30
        except FileNotFoundError:
            return None, 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        return None, elapsed_time
