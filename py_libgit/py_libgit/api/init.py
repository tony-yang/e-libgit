import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.head_ref import HeadRef
from py_libgit.core.objects import Objects
from py_libgit.core.refs import Refs
from py_libgit.core.repo import Repo

class Init:
    def __init__(self, repo_name):
        logger.info('Create the Init object')
        self.repo_name = repo_name

    def create_git_repo(self):
        self.repo = Repo()
        self.repo.create_repo(self.repo_name)
        self.objects = Objects(self.repo_name)
        self.refs = Refs(self.repo_name)
        self.head_ref = HeadRef(self.repo_name)
