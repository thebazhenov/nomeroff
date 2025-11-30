def f(a,b = None, c = None):
    if c: return 2
    if b: return 1
    return 0
    return 3

print(f(3,3))