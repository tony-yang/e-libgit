import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os
from py_libgit.core.index import Index
from py_libgit.core.index_entry import IndexEntry
from py_libgit.core.object_blob import ObjectBlob

class Objects:
    def __init__(self, repo):
        logger.info('Create an Objects object')
        self.pwd = os.getcwd()
        self.repo = repo

    def create_objects_dir(self, repo_name, bare_repo=False):
        '''Create the objects directory for holding the git objects

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        if bare_repo:
            objects_dir = os.path.join(self.pwd, repo_name, 'objects')
        else:
            objects_dir = os.path.join(self.pwd, repo_name, '.git', 'objects')

        os.makedirs(objects_dir, mode=0o644)

    def create_objects(self, pathname):
        pwd = os.getcwd()
        full_pathname = os.path.join(pwd, pathname)
        blob_object = ObjectBlob(self.repo)
        index = Index(self.repo)

        staging_content = []

        if os.path.isfile(full_pathname):
            content_hash = blob_object.create_blob_object(full_pathname)
            staging_content.append(IndexEntry(full_pathname, new_sha1=content_hash))
        elif os.path.isdir(full_pathname):
            pathname = full_pathname
            for dirpath, subdir, filenames in os.walk(pathname):
                # The .git directory is used for git repo management
                # Git's index should never track this directory
                if '.git' in dirpath:
                    continue

                logger.info('Creating blob object by accessing dirpath = {} and subdir = {} and filenames = {}'.format(dirpath, subdir, filenames))
                for filename in filenames:
                    full_pathname = os.path.join(dirpath, filename)
                    content_hash = blob_object.create_blob_object(full_pathname)
                    staging_content.append(IndexEntry(full_pathname, new_sha1=content_hash))

        index.update_index(staging_content)
        return content_hash
