#!/usr/bin/env python2

def read_file():
    try:
        filename = raw_input("Enter the file name: ")
        with open(filename, 'r') as file:
            for line in file:
                print line.rstrip()
    except IOError as e:
        print "Error: Could not read file. %s" % e
    except Exception as e:
        print "An unexpected error occurred: %s" % e

if __name__ == "__main__":
    read_file()

