import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os, re
from py_libgit.core.head_ref import HeadRef
from py_libgit.core.index import Index
from py_libgit.core.objects import Objects
from py_libgit.core.refs import Refs
from py_libgit.core.exceptions import FileNamingConventionError
from py_libgit.core.exceptions import NotGitRepoError

class Repo:
    def __init__(self):
        logger.info('Create a new Repo')
        self.pwd = os.getcwd()
        self.index = Index(self)
        self.objects = Objects(self, self.index)
        self.refs = Refs()
        self.head_ref = HeadRef()

    def verify_naming_convention(self, repo_name):
        '''Verify if the repository name follows convention. File name should only contain letters, digits, _, ., and -

        Keyword arguments:
        repo_name -- the name of the repository
        '''
        name_regex = re.compile(r'[^a-zA-Z0-9_.-]')
        if bool(name_regex.search(repo_name)):
            raise FileNamingConventionError(repo_name, 'File name should only contain letters, digits, _, ., and -')

        return True

    def repo_exist(self, repo_name):
        if os.path.exists(os.path.join(self.pwd, repo_name)):
            raise FileExistsError('The git repository {} already exists!'.format(repo_name))
        return False

    def create_repo(self, repo_name, bare_repo=False):
        '''Create a new repo

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        self.verify_naming_convention(repo_name)
        self.repo_exist(repo_name)

        if not bare_repo:
            git_repo = os.path.join(self.pwd, repo_name, '.git')
            os.makedirs(git_repo, mode=0o644)

        self.objects.create_objects_dir(repo_name, bare_repo)
        self.refs.create_refs_dir(repo_name, bare_repo)
        self.head_ref.create_head_ref_file(repo_name, bare_repo)

    def get_repo_root(self, current_dir):
        while not os.path.exists(os.path.join(current_dir, '.git')):
            current_dir = os.path.dirname(current_dir)
            if '/' == current_dir:
                raise NotGitRepoError(current_dir, 'Not a git repository. Please run `git init` at the top-most level of this project')
        current_dir = os.path.join(current_dir, '.git')
        return current_dir

    def add_objects(self, pathname):
        blob_hash = self.objects.create_objects(pathname)
        return blob_hash

    def create_tree(self):
        return self.objects.create_cached_tree_objects()

    def create_commit(self, author, message, root_tree_entry):
        current_head_sha1 = [self.head_ref.get_current_head_sha1(self)]
        new_commit_sha1 = self.objects.create_commit(author, message, root_tree_entry, current_head_sha1)
        self.head_ref.update_head_ref(self, new_commit_sha1)
        return new_commit_sha1
