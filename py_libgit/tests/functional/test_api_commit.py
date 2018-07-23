import unittest

import os, shutil
from py_libgit.api.add import Add
from py_libgit.api.commit import Commit
from py_libgit.api.init import Init

import py_libgit.settings_tests

class TestCommit(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')
        self.repo_name = 'hellogit-testrepo'

        self.init = Init()
        self.init.create_git_repo(self.repo_name)

        self.add = Add()
        filename = 'hello'
        content = 'hello world\n'
        pwd = os.getcwd()
        os.chdir(os.path.join(pwd, self.repo_name))
        with open(filename, 'w') as f:
            f.write(content)
        content_hash = self.add.create_blob(filename)

        self.commit = Commit()

    def tearDown(self):
        os.chdir('/tmp')
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_commit_successfully(self):
        commit_hash = self.commit.create_commit()
        self.assertEqual(commit_hash, '123', 'Incorrect commit hash')