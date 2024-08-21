from functools import reduce

# Q1: Fibonacci Sequence Generator
fib = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n-2), [0, 1])[:n]
# Test:
print(fib(10))

# Q2: Strings concatenation
concat_Strings = lambda lst: reduce(lambda x, y: x + " " + y, lst)
# Test:
print(concat_Strings(["This", "is", "a", "test"]))

# Q3: Square list
def sum_of_squares(lst):
    return list(map(
        lambda sublist: reduce(
            lambda accumulator , x: accumulator + x,
            map(
                lambda y: y**2,
                filter(
                    lambda z: z % 2 == 0,
                    sublist
                )
            ),
            0
        ),
        lst
    ))


# Test:
lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum_of_squares(lists))


# Q4: Higher-Order Function for Cumulative Operations
def cumulative_operation(op):
    return lambda seq: reduce(op, seq)


# Multiplication
mult = lambda x, y: x * y
# Factorial using cumulative_operation
factorial = lambda n: cumulative_operation(mult)(range(1, n + 1))
# Exponentiation (repeated multiplication)
exponentiate = lambda x, y: x ** y
# Exponentiation using cumulative_operation
exponentiation = lambda base, exp: cumulative_operation(exponentiate)([base] * exp)


def test_cumulative_factorial_and_exp_operations(n, base, exp):
    factorial_res = factorial(n)
    exponentiation_res = exponentiation(base, exp)
    print(f"Factorial function res: {factorial_res}")
    print(f"Exponentiation function res: {exponentiation_res}")


# Test
test_cumulative_factorial_and_exp_operations(4, 3,3)


# Q5
sum_squared = lambda nums: reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))

# Test:
print(sum_squared([1, 2, 3, 4, 5, 6]))

# Q6 Return a list of numbers of the palindromes strings:
count_palindromes = lambda lst: list(map(lambda sublist: reduce(lambda x, y: x + (1 if y == y[::-1] else 0), sublist, 0), lst))

# Test:
str_lst = [["civic", "burger", "rotor"], ["morning", "cat", "python"], ["noon", "def"]]
print(count_palindromes(str_lst))


# Q8 Prime numbers list:
calc_primes_desc = lambda nums: sorted([n for n in nums if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))], reverse=True)

# Test:
all_numbers = [30, 3, 24, 7, 11, 16, 13, 19]
only_primes_desc = calc_primes_desc(all_numbers)
print(only_primes_desc)
