#!/usr/bin/env python
import argparse
from py_libgit.core.init import Init

import pprint
pp = pprint.PrettyPrinter(indent=4)

def main():
    print('Calling git main()')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', metavar='COMMAND', nargs='?', help='Common git command')
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    elif 'init' == args.command:
        pass


if __name__ == '__main__':
    main()
