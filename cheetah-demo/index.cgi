#!/usr/local/bin/python

from Cheetah.Template import Template

from random import randint


def main():
   random = randint(0, 100)

   print "Content-Type: text/html"
   print

   page = Template(file="index.tmpl", searchList=[locals()])
   print page.respond()

if __name__ == "__main__":
   main()
