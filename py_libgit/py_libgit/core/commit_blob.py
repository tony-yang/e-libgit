import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import hashlib, os
from py_libgit.core.commit_entry import CommitEntry

class CommitBlob:
    def __init__(self, repo):
        logger.info('Create an Commit object')
        self.repo = repo

    def create_hash(self, commit_entry):
        content_str = 'tree: {}\nparents: {}\nauthor: {}\nmessage: {}'.format(
            commit_entry.root_tree_sha1,
            commit_entry.parents_sha1,
            commit_entry.author,
            commit_entry.message
        )
        logger.info('Commit entry = {}'.format(content_str))
        content_hash = hashlib.sha1(content_str.encode()).hexdigest()
        logger.info('Hash of commit entry = {}'.format(content_hash))
        return content_hash

    def store_commit_blob(self, commit_hash, commit_entry):
        logger.info('In dir = {}'.format(os.getcwd()))
        root_dir = self.repo.get_repo_root(os.getcwd())
        object_dir = os.path.join(root_dir, 'objects', commit_hash[:2])
        object_basename = commit_hash[2:]
        full_path = os.path.join(object_dir, object_basename)
        if os.path.exists(full_path):
            raise BlobHashConflictError(content_hash, 'There is a conflict in blob hash. This will cause information loss.')
        else:
            logger.info('Create a new blob hash with hash = {} at dir = {}'.format(commit_hash, object_dir))
            os.makedirs(object_dir, mode=0o644, exist_ok=True)

        with open(full_path, 'w') as f:
            content = 'tree: {}\nparents: {}\nauthor: {}\nmessage: {}'.format(
                commit_entry.root_tree_sha1,
                commit_entry.parents_sha1,
                commit_entry.author,
                commit_entry.message
            )
            f.write(content)

    def create_commit(self, commit_entry):
        logger.info('Create a new commit message')
        commit_hash = self.create_hash(commit_entry)
        self.store_commit_blob(commit_hash, commit_entry)
        return commit_hash
