#!/usr/bin/python

class ref:
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj

print "a=ref([1, 2])\nb=a"
a = ref([1, 2])
b = a
print "a.get():" 
print a.get()  # => [1, 2]
print "b.get():" 
print b.get()  # => [1, 2]

print "b.set(4)"
b.set(4)
print "a.get():" 
print a.get()  # => 2
print "a.get():" 
print b.get()  # => 2

