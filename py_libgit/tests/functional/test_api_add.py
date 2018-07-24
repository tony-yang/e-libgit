import unittest

import os, shutil
from py_libgit.api.add import Add
from py_libgit.api.init import Init

import py_libgit.settings_tests

class TestAdd(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')
        self.repo_name = 'hellogit-testrepo'
        self.add = Add()
        self.init = Init()
        self.init.create_git_repo(self.repo_name)

        self.filename = 'hello'
        self.pwd = os.getcwd()
        content = 'hello world\n'
        os.chdir(os.path.join(self.pwd, self.repo_name))
        with open(self.filename, 'w') as f:
            f.write(content)

    def tearDown(self):
        os.chdir('/tmp')
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_blob_successfully(self):
        content_hash = self.add.create_blob(self.filename)
        self.assertEqual(content_hash, '22596363b3de40b06f981fb85d82312e8c0ed511', 'Incorrect blob hash')

        object_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
        object_blob = os.path.exists(object_blob_path)
        self.assertTrue(object_blob, 'The hello object is not created under the object directory')

    def test_add_same_blob_twice_successfully(self):
        content_hash = self.add.create_blob(self.filename)
        content_hash = self.add.create_blob(self.filename)
        self.assertEqual(content_hash, '22596363b3de40b06f981fb85d82312e8c0ed511', 'Incorrect blob hash')

        object_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
        object_blob = os.path.exists(object_blob_path)
        self.assertTrue(object_blob, 'The hello object is not created under the object directory')

    def test_add_using_shell_wildcard_glob(self):
        shell_glob = '.'
        content_hash = self.add.create_blob(shell_glob)
        self.assertEqual(content_hash, '22596363b3de40b06f981fb85d82312e8c0ed511', 'Incorrect blob hash')

        object_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
        object_blob = os.path.exists(object_blob_path)
        self.assertTrue(object_blob, 'The hello object is not created under the object directory')

        git_HEAD_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '7b', 'eb154244f8644b1f14114de8a1acc836d67e88')
        HEAD_blob = os.path.exists(git_HEAD_blob_path)
        self.assertFalse(HEAD_blob, 'The HEAD object should not be tracked and created under the object directory')

    def test_add_twice_using_shell_wildcard_glob(self):
        shell_glob = '.'
        content_hash = self.add.create_blob(shell_glob)
        content_hash = self.add.create_blob(shell_glob)
        self.assertEqual(content_hash, '22596363b3de40b06f981fb85d82312e8c0ed511', 'Incorrect blob hash')

        object_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
        object_blob = os.path.exists(object_blob_path)
        self.assertTrue(object_blob, 'The hello object is not created under the object directory')

        git_HEAD_blob_path = os.path.join(self.pwd, self.repo_name, '.git', 'objects', '7b', 'eb154244f8644b1f14114de8a1acc836d67e88')
        HEAD_blob = os.path.exists(git_HEAD_blob_path)
        self.assertFalse(HEAD_blob, 'The HEAD object should not be tracked and created under the object directory')
