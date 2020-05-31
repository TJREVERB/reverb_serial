from serial import Serial

s = Serial(port = "test")
s.write("hello friends")
print(s.read())
