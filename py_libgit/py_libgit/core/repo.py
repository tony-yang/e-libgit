import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os, re
from py_libgit.core.head_ref import HeadRef
from py_libgit.core.objects import Objects
from py_libgit.core.refs import Refs
from py_libgit.core.exceptions import FileNamingConventionError

class Repo:
    def __init__(self):
        logger.info('Create a new Repo')
        self.pwd = os.getcwd()
        self.objects = Objects()
        self.refs = Refs()
        self.head_ref = HeadRef()

    def verify_naming_convention(self, repo_name):
        name_regex = re.compile(r'[^a-zA-Z0-9_.-]')
        if bool(name_regex.search(repo_name)):
            raise FileNamingConventionError(repo_name, 'File name should only contain letters, digits, _, ., and -')

        return True

    def create_repo(self, repo_name):
        self.verify_naming_convention(repo_name)
        git_repo = os.path.join(self.pwd, repo_name, '.git')
        os.makedirs(git_repo, mode=0o644)

        self.objects.create_objects_dir(repo_name)
        self.refs.create_refs_dir(repo_name)
        self.head_ref.create_head_ref_file(repo_name)

    def create_bare_repo(self, repo_name):
        self.verify_naming_convention(repo_name)

        self.objects.create_objects_dir(repo_name, bare_repo=True)
        self.refs.create_refs_dir(repo_name, bare_repo=True)
        self.head_ref.create_head_ref_file(repo_name, bare_repo=True)
