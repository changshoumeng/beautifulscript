x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4}

# merging two dicts.

z = {**x, **y}
print(z)
print({*x})

import random, string
pwd=''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))
print(pwd)


