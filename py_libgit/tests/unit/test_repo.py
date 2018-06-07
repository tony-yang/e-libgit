import unittest
from unittest.mock import MagicMock
import os, shutil

from py_libgit.api.init import Init
from py_libgit.core.repo import Repo
from py_libgit.core.exceptions import FileNamingConventionError
from py_libgit.core.exceptions import NotGitRepoError

# Make sure this is after all other import to override the logger setting
import py_libgit.settings_tests

class TestRepo(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')
        self.repo_name = 'hello-git'
        self.init = Init()
        self.init.create_git_repo(self.repo_name)
        self.git_repo = Repo()

    def tearDown(self):
        os.chdir('/tmp')
        full_path = os.path.join('/tmp', self.repo_name)
        shutil.rmtree(full_path, ignore_errors=True)

    def test_good_repo_name_should_return_true(self):
        good_name = self.git_repo.verify_naming_convention(self.repo_name)
        self.assertTrue(good_name, 'The repo name is valid with [a-zA-Z0-9_.-] but failed to validate')

    def test_bad_repo_name_should_raise_exception(self):
        with self.assertRaises(FileNamingConventionError, msg='The repo name is invalid with special character. Only [a-zA-Z0-9_.-] are allowed'):
            repo_name = 'hello-git*'
            self.git_repo.verify_naming_convention(repo_name)

    def test_duplicate_repo_name_should_raise_exception(self):
        real_os_path_exists = os.path.exists
        os.path.exists = MagicMock(return_value=True)
        with self.assertRaises(FileExistsError, msg='The git repository hello-git already exists!'):
            self.git_repo.repo_exist(self.repo_name)

        os.path.exists = real_os_path_exists

    def test_get_repo_root_when_git_at_the_current_directory_level(self):
        full_path = os.path.join('/tmp', self.repo_name)
        os.chdir(full_path)
        repo_root_dir = self.git_repo.get_repo_root(full_path)
        expected_path = os.path.join(full_path, '.git')
        self.assertEqual(expected_path, repo_root_dir)

    def test_get_repo_root_on_a_non_git_repo_should_raise_exception(self):
        non_git_dir = '/tmp/non-repo'
        os.makedirs(non_git_dir)
        os.chdir(non_git_dir)

        with self.assertRaises(NotGitRepoError, msg='Not a git repository. Please run `git init` at the top-most level of this project'):
            self.git_repo.get_repo_root(non_git_dir)

        os.chdir('/tmp')
        shutil.rmtree(non_git_dir, ignore_errors=True)
