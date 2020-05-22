from karel_the_robot import World, Robot

#https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6

# No trickery. Class A has no methods nor variables.
a = Robot(0, 0, 0, 0)
try:
    a.foo()
except AttributeError as ae:
    print(f'Exception caught: {ae}')  # 'A' object has no attribute 'foo'

try:
    a.bar('The quick brown fox jumped over the lazy dog.')
except AttributeError as ae:
    print(f'Exception caught: {ae}')  # 'A' object has no attribute 'bar'


# Non-decorator way (note the function must accept self)
# def foo(self):
#     print('hello world!')
# setattr(A, 'foo', foo)

# def bar(self, s):
#     print(f'Message: {s}')
# setattr(A, 'bar', bar)

# Decorator can be written to take normal functions and make them methods
@Robot.add_method(Robot)
def foo():
    print('hello world!')


@Robot.add_method(Robot)
def bar(s):
    foo()
    print(s)


a.foo()
a.bar('The quick brown fox jumped over the lazy dog.')
print(a.foo)  # <bound method foo of <__main__.A object at {ADDRESS}>>
print(a.bar)  # <bound method bar of <__main__.A object at {ADDRESS}>>

# foo and bar are still usable as functions
foo()
bar('The quick brown fox jumped over the lazy dog.')
print(foo)  # <function foo at {ADDRESS}>
print(bar)  # <function bar at {ADDRESS}>
