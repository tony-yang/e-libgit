import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import hashlib, os
from py_libgit.core.exceptions import BlobHashConflictError
from py_libgit.core.index import Index


class Object:
    def __init__(self, repo):
        logger.info('Create a new Object object')
        self.repo = repo

    def create_hash(self, content):
        logger.info('content = {}'.format(content))
        content_hash = hashlib.sha1(content.encode()).hexdigest()
        logger.info('hash of content = {}'.format(content_hash))
        return content_hash

    def track_pathname_in_index(self, pathname):
        index = Index(self.repo)
        index.update_index(pathname)

    def store_blob(self, content_hash, content):
        logger.info('In dir = {}'.format(os.getcwd()))
        root_dir = self.repo.get_repo_root(os.getcwd())
        object_dir = os.path.join(root_dir, 'objects', content_hash[:2])
        if os.path.exists(object_dir):
            raise BlobHashConflictError(content_hash, 'There is a conflict in blob hash. This will cause information loss')
        else:
            logger.info('Create a new blob hash with hash = {} at dir = {}'.format(content_hash, object_dir))
            os.makedirs(object_dir)
            object_basename = content_hash[2:]
            full_path = os.path.join(object_dir, object_basename)
            logger.info('Creating object blob at = {}'.format(full_path))
            with open(full_path, 'w') as f:
                f.write(content)

    def create_blob_object(self, pathname):
        if os.path.isfile(pathname):
            with open(pathname, 'r') as f:
                content = f.read()
                content_hash = self.create_hash(content)
                self.store_blob(content_hash, content)
                self.track_pathname_in_index(pathname)
        elif os.path.isdir(pathname):
            for dirpath, subdir, filenames in os.walk(pathname):
                # The .git directory is used for git repo management
                # It should never track this directory
                logger.info('Creating blob object by accessing dirpath = {} and subdir = {} and filenames = {}'.format(dirpath, subdir, filenames))
                if '.git' in dirpath:
                    continue

                for filename in filenames:
                    full_pathname = os.path.join(dirpath, filename)
                    content_hash = self.create_blob_object(full_pathname)

        return content_hash
