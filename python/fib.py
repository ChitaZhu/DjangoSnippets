# /usr/bin/env python
# -*- coding:utf-8 -*-

def fib(max):
    a, b = 0, 1 
    arr = [0, 1]
    if max > 0 and max <=2:
        return arr[:max]
    elif max > 2:
        while len(arr) < max:
            [a, b] = [b, a+b]
            arr.append(b)
        return arr
    else:
        print("max错误,须大于0.")

def fib1(max):
    a, b = 0, 1
    n = 0
    if max <= 0: print("max错误,须大于0.")
    while n < max:
        yield a
        n += 1
        a , b = [b, a+b] 


if __name__ == "__main__":
    print(fib(0))
    print(fib(1))
    print(fib(2))
    print(fib(10))
    f = fib1(10)
    # print(f)
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    # print(next(f))
    for item in f:
        print(item)

import functools
### 装饰器，不接受参数
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print("%s()" % func.__name__)
        return func(*args, **kw)
    return wrapper

### 装饰器，接受参数
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("%s %s():" % (text, func.__name__))
        return func(*args, **kw)
    return wrapper

@log('execute')
def now():
    print("2020-04-08")

# 等效 now = log('execute')(now)
# 返回顺序：decoractor函数 -> 调用返回的函数 -> wrapper