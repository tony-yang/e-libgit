import unittest
from unittest.mock import MagicMock


import hashlib, os, shutil
from py_libgit.core.exceptions import BlobHashConflictError
from py_libgit.core.object import Object

import py_libgit.settings_tests

class TestObject(unittest.TestCase):
    def setUp(self):
        self.git_repo = '/tmp/objects-repo'
        self.git_root_dir = os.path.join(self.git_repo, '.git')
        self.objects_dir = os.path.join(self.git_root_dir, 'objects')

        repo = MagicMock()
        repo.get_repo_root = MagicMock(return_value=self.git_root_dir)
        os.makedirs(self.objects_dir)
        os.chdir(self.objects_dir)

        self.obj = Object(repo)

    def tearDown(self):
        shutil.rmtree(self.git_repo, ignore_errors=True)

    def test_store_blob_on_new_blob_hash_will_succeed(self):
        content = 'hello world\n'
        content_hash = hashlib.sha1(content.encode()).hexdigest()
        self.obj.store_blob(content_hash, content)

        filename = os.path.join(content_hash[:2], content_hash[2:])
        blob_file = os.path.exists(os.path.join(self.objects_dir, filename))
        self.assertTrue(blob_file)

    def test_store_blob_on_existing_blob_should_raise_exception(self):
        content = 'hello world\n'
        content_hash = hashlib.sha1(content.encode()).hexdigest()

        real_os_path_exists = os.path.exists
        os.path.exists = MagicMock(return_value=True)
        with self.assertRaises(BlobHashConflictError, msg='There is a conflict in blob hash. This will cause information loss'):
            self.obj.store_blob(content_hash, content)

        os.path.exists = real_os_path_exists
