import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.repo import Repo

class Init:
    def __init__(self):
        logger.info('Create the Init object')

    def create_git_repo(self, repo_name, bare_repo=False):
        '''Create a new git repository

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        self.repo_name = repo_name
        self.repo = Repo()
        try:
            self.repo.create_repo(self.repo_name, bare_repo)
        except FileExistsError:
            logger.warning('The git repository {} already exists!'.format(self.repo_name))
            print('The git repository {} already exists!'.format(self.repo_name))
