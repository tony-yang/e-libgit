import unittest

import hashlib, os, shutil
from py_libgit.api.add import Add
from py_libgit.api.commit import Commit
from py_libgit.api.init import Init
from py_libgit.api.tree import Tree
from py_libgit.core.tree_entry import TreeEntry, EntryType

import py_libgit.settings_tests

class TestCommit(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')
        self.repo_name = 'hellogit-testrepo'

        self.init = Init()
        self.init.create_git_repo(self.repo_name)

        add = Add()
        filename = 'hello'
        content = 'hello world\n'
        pwd = os.getcwd()
        os.chdir(os.path.join(pwd, self.repo_name))
        with open(filename, 'w') as f:
            f.write(content)
        content_hash = add.create_blob(filename)

        tree = Tree()
        self.tree_entry = tree.create_tree()

        self.commit = Commit()

    def tearDown(self):
        os.chdir('/tmp')
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_commit_successfully(self):
        author = 'name author'
        message = 'test commit message for hello world'

        commit_hash = self.commit.create_commit(author=author, commit_message=message, root_tree_entry=self.tree_entry)
        expected_commit_entry = 'tree: 6a98fd9cb9c98a860866e8a309f51c0686baa3e8\nparents: []\nauthor: name author\nmessage: test commit message for hello world'
        expected_commit_sha1 = hashlib.sha1(expected_commit_entry.encode()).hexdigest()
        self.assertEqual(commit_hash, expected_commit_sha1, 'Incorrect commit hash when create the commit')

        expected_commit_object_path = os.path.join(os.getcwd(), '.git', 'objects', commit_hash[:2], commit_hash[2:])
        commit_object_exists = os.path.exists(expected_commit_object_path)
        self.assertTrue(commit_object_exists)
