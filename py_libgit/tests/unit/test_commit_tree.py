import unittest
from unittest.mock import MagicMock

import hashlib, os, shutil
from py_libgit.core.commit_tree import CommitTree
from py_libgit.core.tree_entry import TreeEntry, EntryType

import py_libgit.settings_tests

class TestCommitTree(unittest.TestCase):
    def setUp(self):
        self.git_repo_name = 'objects-repod'
        self.git_repo = os.path.join('/tmp', self.git_repo_name)
        self.git_root_dir = os.path.join(self.git_repo, '.git')
        self.objects_dir = os.path.join(self.git_root_dir, 'objects')
        self.repo = MagicMock()
        self.repo.get_repo_root = MagicMock(return_value=self.git_root_dir)
        os.makedirs(self.objects_dir)
        os.chdir(self.objects_dir)

    def tearDown(self):
        shutil.rmtree(self.git_repo, ignore_errors=True)

    def test_commit_one_level_tree_returns_the_correct_tree_entry(self):
        root = CommitTree(self.repo, TreeEntry(self.git_repo_name, entry_type=EntryType.TREE))
        subtree = CommitTree(self.repo, TreeEntry('hello', entry_type=EntryType.BLOB, sha1='0123456789'*4))
        root.add_subtree(subtree)

        subtree_content = '{},{},{},{}\n'.format(subtree.tree_entry.name, subtree.tree_entry.unix_mode, subtree.tree_entry.entry_type, subtree.tree_entry.sha1)
        subtree_hash = hashlib.sha1(subtree_content.encode()).hexdigest()

        tree_entry = root.commit_tree_blob()
        expected_file_path = os.path.join(self.objects_dir, subtree_hash[:2], subtree_hash[2:])
        self.assertTrue(os.path.exists(expected_file_path))
        expected_root_entry = root.tree_entry
        expected_root_entry.sha1 = subtree_hash
        self.assertEqual(tree_entry, expected_root_entry, 'The commit returned incorrect tree entry at the root level')

    def test_commit_multi_level_tree_returns_the_correct_tree_entry(self):
        leaf_tree = CommitTree(self.repo, TreeEntry('hello', entry_type=EntryType.BLOB, sha1='0123456789'*4))
        leaf_tree_content = '{},{},{},{}\n'.format(leaf_tree.tree_entry.name, leaf_tree.tree_entry.unix_mode, leaf_tree.tree_entry.entry_type, leaf_tree.tree_entry.sha1)
        leaf_tree_hash = hashlib.sha1(leaf_tree_content.encode()).hexdigest()

        subtree = CommitTree(self.repo, TreeEntry('hellodir', entry_type=EntryType.TREE, sha1=leaf_tree_hash))
        subtree.add_subtree(leaf_tree)
        subtree_content = '{},{},{},{}\n'.format(subtree.tree_entry.name, subtree.tree_entry.unix_mode, subtree.tree_entry.entry_type, subtree.tree_entry.sha1)
        subtree_hash = hashlib.sha1(subtree_content.encode()).hexdigest()

        root = CommitTree(self.repo, TreeEntry(self.git_repo_name, entry_type=EntryType.TREE, sha1=subtree_hash))
        root.add_subtree(subtree)

        tree_entry = root.commit_tree_blob()
        expected_file_path = os.path.join(self.objects_dir, subtree_hash[:2], subtree_hash[2:])
        self.assertTrue(os.path.exists(expected_file_path))

        expected_root_entry = root.tree_entry
        self.assertEqual(tree_entry, expected_root_entry, 'The commit returned incorrect tree entry at the root level for multi-level trees')
