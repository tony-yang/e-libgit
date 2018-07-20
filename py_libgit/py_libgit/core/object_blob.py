import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import hashlib, os
from py_libgit.core.exceptions import BlobHashConflictError


class ObjectBlob:
    def __init__(self, repo):
        logger.info('Create a new Object object')
        self.repo = repo

    def create_hash(self, content):
        logger.info('content = {}'.format(content))
        content_hash = hashlib.sha1(content.encode()).hexdigest()
        logger.info('hash of content = {}'.format(content_hash))
        return content_hash

    def store_blob(self, content_hash, content):
        logger.info('In dir = {}'.format(os.getcwd()))
        root_dir = self.repo.get_repo_root(os.getcwd())
        object_dir = os.path.join(root_dir, 'objects', content_hash[:2])
        object_basename = content_hash[2:]
        full_path = os.path.join(object_dir, object_basename)
        if os.path.exists(full_path):
            raise BlobHashConflictError(content_hash, 'There is a conflict in blob hash. This will cause information loss.')
        else:
            logger.info('Create a new blob hash with hash = {} at dir = {}'.format(content_hash, object_dir))
            os.makedirs(object_dir, mode=0o644, exist_ok=True)
            logger.info('Creating object blob at = {}'.format(full_path))
            with open(full_path, 'w') as f:
                f.write(content)

    def create_blob_object(self, filename):
        if not os.path.isfile(filename):
            raise IsADirectoryError

        with open(filename, 'r') as f:
            content = f.read()
            content_hash = self.create_hash(content)
            try:
                self.store_blob(content_hash, content)
            except BlobHashConflictError:
                # In this case, we treat it as the same content
                # Do nothing and continue
                pass

        return content_hash
