import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os
from py_libgit.core.index_entry import IndexEntry

class Index:
    def __init__(self, repo):
        logger.info('Create an Index object')
        self.repo = repo

    def build_tracked_index(self):
        git_root = self.repo.get_repo_root(os.getcwd())
        index_file = os.path.join(git_root, 'index')
        tracked_index = {}

        if not os.path.exists(index_file):
            return {}

        # The index file format
        # pathname current_sha1 staged_sha1 unix_mode
        with open(index_file, 'r') as files:
            for item in files:
                file_attributes = item.split()
                tracked_index[file_attributes[0].strip()] = IndexEntry(
                    pathname=file_attributes[0].strip(),
                    current_sha1=file_attributes[1].strip(),
                    new_sha1=file_attributes[2].strip(),
                    unix_mode=file_attributes[3].strip()
                    )
        return tracked_index

    def update_index(self, index_content=[]):
        git_root = self.repo.get_repo_root(os.getcwd())
        index_file = os.path.join(git_root, 'index')
        tracked_index = {}
        if os.path.exists(index_file):
            tracked_index = self.build_tracked_index()
            
        for index_entry in index_content:
            pathname = self.normalize_pathname(index_entry.pathname)
            # The index file format
            # pathname current_sha1 staged_sha1 unix_mode
            # current_sha1 is 0 for new file
            tracked_index[pathname] = IndexEntry(
                pathname=pathname,
                current_sha1=index_entry.current_sha1,
                new_sha1=index_entry.new_sha1,
                unix_mode=index_entry.unix_mode
            )

        with open(index_file, 'w') as f:
            for pathname in sorted(tracked_index):
                index_entry = tracked_index[pathname]
                f.write('{} {} {} {}\n'.format(pathname, index_entry.current_sha1, index_entry.new_sha1, index_entry.unix_mode))

    def normalize_pathname(self, pathname):
        git_root = self.repo.get_repo_root(os.getcwd())
        repo_dirs = os.path.dirname(git_root).split('/')
        repo_name = repo_dirs[-1]
        pathes = pathname.split('/')
        repo_name_index = 0
        for i, item in enumerate(pathes):
            if item == repo_name:
                repo_name_index = i
                break

        reduced_pathes = []
        while repo_name_index < len(pathes):
            item = pathes[repo_name_index]
            if item and item == '..':
                reduced_pathes.pop()
            elif item and item != '.':
                reduced_pathes.append(item)
            repo_name_index += 1
        normalized_path = '/'.join(reduced_pathes)
        return normalized_path
