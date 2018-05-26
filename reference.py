# python reference

# basic operations
print(5 / 3) # x is a float
print(5 // 3) # floor division
print(-5 % 3) # returns +ve remainder
print(2 ** 4) # exponent
print('')

#########################################################

# strings
x = "asd"
y = 'asd' # single or double quotes
x = 'don\'t' # backslash

# printing raw
print(r'C:\some\name' + '\n');

# print literal
print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""" + '\n')

# string multiplication and concat
# multiplication takes precedence
print(3 * "thrice" + 2 * "twice" + '\n')

# string slicing
word = '012345'
print('word[0] = ' + word[0])
print('word[3] = ' + word[3])
print('word[-2] = ' + word[-2])
print('word[1:4] = ' + word[1:4]) # exclusive of last index
print('word[3:] = ' + word[3:])
print(len(word))
print('')

#########################################################

# lists
xs = [1, 4, 9, 16, 25, 36, 49]
print(*xs, sep = ', ') # print list wtih *
print('str() method:', str(xs))
print('xs[0] = {}'.format(xs[0]))
print('xs[-1] = {}'.format(xs[-1]))
print('xs[2:] = {}'.format(xs[2:]))
print('shallow copy = xs[:] = {}'.format(xs[:]))

# list operations
xs = ['a', 'b', 'c', 'd', 'e', 'f']
xs.append('g') # assignment
xs[2:5] = ['C', 'D', 'E'] # slice + assignment
len(xs) # length

# creating list from range
xs = list(range(5, 16))
print('xs =', str(xs), '\n')

#########################################################

# if else

x = 3
if x < 0:
    print('a')
elif x == 0:
    print('b')
else:
    print('c')

#########################################################

# for loop
for i in range(5):
    print(i)
print('')
    
for i in range(3, 11, 2): # excludes end
    print(i)
print('')

# enhanced for loop
xs = [1, 2, 3, 4, 5]
print('for loop 1')
for i in xs:
    print(i)

print('for loop 2')
for i in xs[1:-1]:
    print(i)

print('')

# for else
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')

# pass
for i in range(3):
    pass
print('')

#########################################################

# defining function

def add(a, b):
    return a + b
print(add(2, 2))

def fib(n):
    """docstring"""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result
print(fib(10))

# note: functions without return stmt return None

def printMsg(msg = 'i love you', times = 4): # default args
    for i in range(times):
        print(msg)
printMsg('u fat', 2)
printMsg(times = 3)
print('')

# can also call with dictionary
d = {'msg' : 'have a nice day', 'times' : 3}
printMsg(**d) # note the **
print('')

# more complicated arg passing
# args is a tuple of variable length, keywords is a dict of variable length
def f(normal, *args, **keywords):
    print('normal', normal)
    print('-' * 40)
    for arg in args:
        print(arg)
    print('-' * 40)
    for kw in keywords:
        print(kw, ':', keywords[kw])
f('hi', 'arg1', 'arg2', 'arg3', key1 = 'key1', key2 = 'key2', key3 = 'key3')    
print('')

def concat(*args, sep=','):
    return sep.join(args)
print(concat('apple', 'banana', 'carrot', 'durian', sep='-'))
print('')

# lambda expressions
def make_incrementor(n):
    return lambda x: x + n
f = make_incrementor(10)
print(f(0), '\n')

pairs = [(3, 'a'), (2, 'c'), (4, 'b'), (1, 'd')]
pairs.sort(key = lambda pair: pair[0])
print(pairs)
pairs.sort(key = lambda pair: pair[1])
print(pairs)
print('')

#########################################################

# list comprehension
print('list comprehension')
sq = list(map(lambda x: x**2, range(10)))
print(*sq)
sq = [x**2 for x in range(10)]
print(*sq)

# list comprehension format: for clause + if clause

crossProduct = [(x,y) for x in ['a','b','c'] for y in [1,2,3] if x != y]
print(crossProduct)

# list operations
xs = [5,6,7]
xs.append(8)
xs.remove(5)
del xs[1]
print(str(xs), '\n')

# looping thru list
print
for i, v in enumerate([1, 3, 5, 7]):
    print(i, v)
print('')

# zip lists
l1 = [1, 2, 3, 4, 5]
l2 = ['a', 'b', 'c', 'd', 'e']
z = zip(l1, l2)
print('z:', *z)
for i, j in zip(l1, l2):
    print('i =', i, '   j =', j)
print('')

#########################################################

# tuple
print('tuple')
t = () # empty
t = 'hi', # singleton
t = 1, 2, 3 # more than 1 item
x, y, z = t # tuple unpacking
print(t)
print('')

# sets
basket = {'A', 'B', 'C'}
a = set('abcdefg')
b = set('aabbcc')
print(a - b) # set minus
print(a | b) # set union
print(a & b) # set intersection
print(a ^ b) # exclusive OR
print('')

# dictionary

# construction
print('dictionary')
d1 = {'key1' : 1, 'key2' : 2, 'key3' : 3}
d1 = dict([('key1', 1), ('key2', 2), ('key3', 3)])
d2 = {('key' + str(x)) : x**2 for x in [1, 2, 3]}
d3 = dict(key1=1, key2=2, key3=3) # if keys are strings
print(d2)

d1['key4'] = 4
d1['key1'] = -1
del d1['key2']
list(d1.keys())
'key1' in d1
print(d1)

# looping thru dict
for k, v in d1.items():
    print(k, v)
print('')

#########################################################

# importing
'''
if:
import fibo #
usage:
fibo.fib(n)

if:
from fibo import fib1, fib2 / from fibo import *
usage:
fib(n)


'''

#########################################################

# class

class Pet:

    classAttr = 'hard' # class attr shared by all instances

    # constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # basic getter
    def getName(self):
        return 'Pet\'s getName method'

    def __str__(self):
        return 'Pet: name={} age={}'.format(self.name, self.age)

    def foo(self): # we want foo to use Pet's getName method
        return self.__getName() # we call a 'private' method

    __getName = getName # initialization of the 'private' method
    

class Dog(Pet):

    def __init__(self, name, color, age = 1):
        # super().__init__(name, age) # alternative using super call
        Pet.__init__(self, name, age)
        self.color = color

    def __str__(self): # overriding
        return 'Dog: name={} age={} color={}'.format(self.name, self.age, self.color)

    def getName(self):
        return 'Dog\'s getName method' # override

x = Pet('tom', 3)
print(x)

# can create attr on the fly
x.fats = 10
print('create on the fly attr', x.fats)
del x.fats # can del attr on the fly
print('')

y = Dog('rob', 'brown')
print('y', y)

# type check
print(isinstance(x, Dog))
print(isinstance(y, Dog))
print('')

print('y.getName():', y.getName())
print('y.foo() (which calls getName())', y.foo())

# generator
def cubes(n): # creates a generator for first n cubes
    for i in range(1, n+1):
        yield i**3
        
# use generator like an iterable
for i in cubes(10):
    print(i)



















