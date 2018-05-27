#!/usr/bin/env python
import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import argparse
from py_libgit.api.init import Init

def main():
    logger.info('Calling git main()')
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init', help='Create an empty Git repository')
    init_parser.add_argument('repo_name', help='New repository name. Should only use letters, digits, _, ., and - in the name')
    init_parser.add_argument('--bare', action='store_true', help='Create a bare repository')
    args = parser.parse_args()

    if 'repo_name' in args:
        logger.info('Called with init repo_name {}'.format(args.repo_name))
        init = Init()
        init.create_git_repo(args.repo_name, args.bare)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
