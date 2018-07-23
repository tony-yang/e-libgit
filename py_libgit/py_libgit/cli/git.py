#!/usr/bin/env python
import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import argparse
from py_libgit.api.add import Add
from py_libgit.api.init import Init
from py_libgit.api.tree import Tree

def main():
    logger.info('Calling git main()')
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    init_parser = subparsers.add_parser('init', help='Create an empty Git repository')
    init_parser.add_argument('repo_name', help='New repository name. Should only use letters, digits, _, ., and - in the name')
    init_parser.add_argument('--bare', action='store_true', help='Create a bare repository')

    add_parser = subparsers.add_parser('add', help='Add new/changed file to the repository')
    add_parser.add_argument('pathname', help='The files or directoies to be added')

    commit_parser = subparsers.add_parser('commit', help='Commit staging changes to the repository')

    args = parser.parse_args()
    if 'init' == args.subparser_name:
        logger.info('Called with init repo_name {}'.format(args.repo_name))
        init = Init()
        init.create_git_repo(args.repo_name, args.bare)
    elif 'add' == args.subparser_name:
        logger.info('Called with add pathname {}'.format(args.pathname))
        add = Add()
        add.create_blob(args.pathname)
    elif 'commit' == args.subparser_name:
        logger.info('Called with commit')
        tree = Tree()
        tree.create_tree()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
