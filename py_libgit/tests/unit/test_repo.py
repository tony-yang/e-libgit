import unittest
from unittest.mock import MagicMock

import logging.config
mockLoggingConfig = logging.config.fileConfig('logging_test.conf')
logging.config.fileConfig = MagicMock(return_value=mockLoggingConfig)

from py_libgit.core.repo import Repo
from py_libgit.core.exceptions import FileNamingConventionError

class TestRepo(unittest.TestCase):
    def test_good_repo_name_should_return_true(self):
        repo_name = 'hello-git'
        git_repo = Repo()
        good_name = git_repo.verify_naming_convention(repo_name)
        self.assertTrue(good_name, 'The repo name is valid with [a-zA-Z0-9_.-] but failed to validate')

    def test_bad_repo_name_should_raise_exception(self):
        with self.assertRaises(FileNamingConventionError, msg='The repo name is invalid with special character. Only [a-zA-Z0-9_.-] are allowed'):
            repo_name = 'hello-git*'
            git_repo = Repo()
            good_name = git_repo.verify_naming_convention(repo_name)
