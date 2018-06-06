import unittest

import os, shutil
from py_libgit.api.add import Add
from py_libgit.api.init import Init

import py_libgit.settings_tests

class TestAdd(unittest.TestCase):
    def setUp(self):
        self.repo_name = 'hellogit-testrepo'
        self.add = Add()
        self.init = Init()
        self.init.create_git_repo(self.repo_name)

    def tearDown(self):
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_blob_successfully(self):
        filename = 'hello'
        content = 'hello world\n'
        pwd = os.getcwd()

        os.chdir(os.path.join(pwd, self.repo_name))
        with open(filename, 'w') as f:
            f.write(content)

        content_hash = self.add.create_blob(filename)
        self.assertEqual(content_hash, '22596363b3de40b06f981fb85d82312e8c0ed511', 'Incorrect blob hash')

        object_blob_path = os.path.join(pwd, self.repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
        object_blob = os.path.exists(object_blob_path)
        self.assertTrue(object_blob)
