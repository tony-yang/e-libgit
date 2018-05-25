import unittest
import os, shutil
from py_libgit.api.init import Init
from py_libgit.core.exceptions import FileNamingConventionError

# Make sure this is after all other import to override the logger setting
import py_libgit.settings_tests

class TestInit(unittest.TestCase):
    def setUp(self):
        self.repo_name = 'hellogit-testrepo'
        self.init = Init(self.repo_name)

    def tearDown(self):
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_git_repo(self):
        self.init.create_git_repo()
        pwd = os.getcwd()

        repo_path = os.path.join(pwd, self.repo_name, '.git')
        repo_dir = os.path.exists(repo_path)

        objects_path = os.path.join(pwd, self.repo_name, '.git', 'objects')
        objects_dir = os.path.exists(objects_path)

        refs_path = os.path.join(pwd, self.repo_name, '.git', 'refs', 'heads')
        refs_dir = os.path.exists(refs_path)

        HEAD_path = os.path.join(pwd, self.repo_name, '.git', 'HEAD')
        HEAD_file = os.path.exists(HEAD_path)

        self.assertTrue(repo_dir, 'Failed to create the .git directory')
        self.assertTrue(objects_dir, 'Failed to create the .git/objects directory')
        self.assertTrue(refs_dir, 'Failed to create the .git/refs/heads directory')
        self.assertTrue(HEAD_file, 'Failed to create the .git/HEAD reference file')

    def test_create_git_repo_with_special_character_should_fail(self):
        repo_name = 'hellogit*'

        with self.assertRaises(FileNamingConventionError, msg='Using special characters in repo name should not be allowed. Only allowing [a-zA-Z0-9_.-] for repo name'):
            git_init = Init(repo_name)
            git_init.create_git_repo()
