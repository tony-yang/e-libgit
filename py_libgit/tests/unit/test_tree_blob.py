import unittest
from unittest.mock import MagicMock

import hashlib, os, shutil
from py_libgit.core.tree_blob import TreeBlob
from py_libgit.core.tree_entry import TreeEntry, EntryType

import py_libgit.settings_tests

class TestTreeBlob(unittest.TestCase):
    def setUp(self):
        self.git_repo = '/tmp/objects-repo'
        self.git_root_dir = os.path.join(self.git_repo, '.git')
        self.objects_dir = os.path.join(self.git_root_dir, 'objects')
        self.repo = MagicMock()
        self.repo.get_repo_root = MagicMock(return_value=self.git_root_dir)
        os.makedirs(self.objects_dir)
        os.chdir(self.objects_dir)

    def tearDown(self):
        shutil.rmtree(self.git_repo, ignore_errors=True)

    def test_create_tree_returns_the_tree_sha1(self):
        entries = [
            TreeEntry('hello', entry_type=EntryType.BLOB, sha1='1234567890'*4)
        ]
        self.tree = TreeBlob(self.repo, entries)

        tree_entry = '{},{},{},{}\n'.format(entries[0].name, entries[0].unix_mode, entries[0].entry_type, entries[0].sha1)
        tree_hash = hashlib.sha1(tree_entry.encode()).hexdigest()

        tree_sha1 = self.tree.create_tree()
        self.assertEqual(tree_sha1, tree_hash, 'The returned tree sha1 is incorrect')

        filename = os.path.join(tree_sha1[:2], tree_sha1[2:])
        tree_blob_file = os.path.exists(os.path.join(self.objects_dir, filename))
        self.assertTrue(tree_blob_file)

    def test_multiple_tree_entries_returns_the_tree_sha1(self):
        entries = [
            TreeEntry('hello', entry_type=EntryType.BLOB, sha1='1234567890'*4),
            TreeEntry('world', entry_type=EntryType.TREE, sha1='9876543210'*4)
        ]
        self.tree = TreeBlob(self.repo, entries)

        tree_entry = '{},{},{},{}\n{},{},{},{}\n'.format(
            entries[0].name,
            entries[0].unix_mode,
            entries[0].entry_type,
            entries[0].sha1,
            entries[1].name,
            entries[1].unix_mode,
            entries[1].entry_type,
            entries[1].sha1
        )
        tree_hash = hashlib.sha1(tree_entry.encode()).hexdigest()

        tree_sha1 = self.tree.create_tree()
        self.assertEqual(tree_sha1, tree_hash, 'The returned tree sha1 for multiple tree entries is incorrect')

        filename = os.path.join(tree_sha1[:2], tree_sha1[2:])
        tree_blob_file = os.path.exists(os.path.join(self.objects_dir, filename))
        self.assertTrue(tree_blob_file)
