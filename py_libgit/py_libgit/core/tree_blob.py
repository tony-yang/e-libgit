import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import hashlib, os
from py_libgit.core.exceptions import BlobHashConflictError

class TreeBlob:
    def __init__(self, repo, entries):
        logger.info('Create the Tree object')
        self.entries = entries
        self.repo = repo

    def create_hash(self, tree_entries):
        logger.info('content = {}'.format(tree_entries))
        content_str = ''
        for entry in tree_entries:
            content_str += '{},{},{},{}\n'.format(entry.name, entry.unix_mode, entry.entry_type, entry.sha1)
        content_hash = hashlib.sha1(content_str.encode()).hexdigest()
        logger.info('hash of content = {}'.format(content_hash))
        return content_hash

    def store_tree_blob(self, tree_hash, tree_entries):
        logger.info('In dir = {}'.format(os.getcwd()))
        root_dir = self.repo.get_repo_root(os.getcwd())
        object_dir = os.path.join(root_dir, 'objects', tree_hash[:2])
        object_basename = tree_hash[2:]
        full_path = os.path.join(object_dir, object_basename)
        if os.path.exists(full_path):
            raise BlobHashConflictError(content_hash, 'There is a conflict in blob hash. This will cause information loss.')
        else:
            logger.info('Create a new blob hash with hash = {} at dir = {}'.format(tree_hash, object_dir))
            os.makedirs(object_dir, mode=0o644, exist_ok=True)
            logger.info('Creating tree blob at = {}'.format(full_path))

            content_str = ''
            for entry in tree_entries:
                content_str += '{},{},{},{}\n'.format(entry.name, entry.unix_mode, entry.entry_type, entry.sha1)

            with open(full_path, 'w') as f:
                f.write(content_str)


    def create_tree(self):
        logger.info('Create a new tree')
        tree_hash = self.create_hash(self.entries)
        try:
            self.store_tree_blob(tree_hash, self.entries)
        except BlobHashConflictError:
            # In this case, we treat it as the same content
            # Do nothing and continue
            pass
        return tree_hash
