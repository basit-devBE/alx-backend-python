
### Python Decorator

Python decorators are a powerful and useful tool in Python that allows programmers to modify the behavior of a function or class. Decorators allow you to wrap another function in order to extend the behavior of the wrapped function, without permanently modifying it.

#### Basic Syntax

A decorator is a function that takes another function as an argument and extends its behavior. Here is a simple example:

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

In this example, `my_decorator` is a decorator that wraps the `say_hello` function. When `say_hello` is called, it will print messages before and after the actual function call.

#### Using Decorators with Arguments

Decorators can also take arguments. Here is an example of a decorator that takes arguments:

```python
def repeat(num_times):
    def decorator_repeat(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                func(*args, **kwargs)
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

greet("Alice")
```

In this example, the `repeat` decorator takes an argument `num_times` and repeats the execution of the `greet` function that many times.

#### Built-in Decorators

Python also provides several built-in decorators such as `@staticmethod`, `@classmethod`, and `@property` which are used to define methods in classes.

Decorators are a very powerful feature in Python and can be used to implement many design patterns and improve code readability and reusability.