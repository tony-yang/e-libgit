import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class Index:
    def __init__(self, repo):
        logger.info('Create an Index object')
        self.repo = repo
        self.git_root = self.repo.get_repo_root(os.getcwd())
        self.index_file = os.path.join(self.git_root, 'index')

    def build_tracked_index(self):
        tracked_index = {}
        with open(self.index_file, 'r') as files:
            for file in files:
                tracked_index[file.strip()] = True
        return tracked_index

    def update_index(self, pathname):
        pathname = self.normalize_pathname(pathname)
        tracked_index = {}
        if os.path.exists(self.index_file):
            tracked_index = self.build_tracked_index()

        if pathname not in tracked_index:
            with open(self.index_file, 'a') as f:
                f.write('{}\n'.format(pathname))

            return True

        return False

    def normalize_pathname(self, pathname):
        repo_dirs = os.path.dirname(self.git_root).split('/')
        repo_name = repo_dirs[-1]
        pathes = pathname.split('/')
        repo_name_index = 0
        for i, item in enumerate(pathes):
            if item == repo_name:
                repo_name_index = i
                break

        reduced_pathes = []
        while i < len(pathes):
            item = pathes[i]
            if item and item == '..':
                reduced_pathes.pop()
            elif item and item != '.':
                reduced_pathes.append(item)
            i += 1
        normalized_path = '/'.join(reduced_pathes)
        return normalized_path
