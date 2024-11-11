import itertools
import string
import time

class Crack:

    def brute_force(self, password):
        chars = string.ascii_lowercase + string.digits
        start_time = time.time()  # Start the timer
        for length in range(1, len(password) + 1):
            for guess in itertools.product(chars, repeat=length):
                guess = ''.join(guess)
                if guess == password:
                    end_time = time.time()  # End the timer
                    elapsed_time = end_time - start_time
                    return guess, elapsed_time
        end_time = time.time()  # End the timer if not found
        elapsed_time = end_time - start_time
        return None, elapsed_time

