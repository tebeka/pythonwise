#!/usr/bin/env python

class Animal(object):
    pass

class Dog(Animal):
    def talk(self):
        return "whoof whoof"

class Cat(Animal):
    def talk(self):
        return "miao"

class Pig(Animal):
    def talk(self):
        return "oink oink"

def all_animals():
    return Animal.__subclasses__()

if __name__ == "__main__":
    for animal in all_animals():
        print "%s says: %s" % (animal.__name__, animal().talk())
