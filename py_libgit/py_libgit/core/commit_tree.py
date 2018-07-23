import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

from py_libgit.core.tree_blob import TreeBlob
from py_libgit.core.tree_entry import EntryType

class CommitTree:
    def __init__(self, repo, tree_entry=None):
        self.tree_entry = tree_entry
        self.subtrees = []
        self.repo = repo

    def add_subtree(self, subtree):
        self.subtrees.append(subtree)

    def add_tree_entry(self, tree_entry):
        self.tree_blob = tree_blob

    def commit_tree_blob(self):
        logger.info('Committing the entire tree structure into objects')
        tree_entries = []
        for subtree in self.subtrees:
            tree_entries.append(subtree.commit_tree_blob())

        if self.tree_entry.entry_type == EntryType.BLOB:
            return self.tree_entry

        tree_blob = TreeBlob(self.repo, tree_entries)
        committed_tree_hash = tree_blob.create_tree()
        self.tree_entry.sha1 = committed_tree_hash
        return self.tree_entry


    def __repr__(self):
        return 'Commit Tree: <tree_entry: {} subtrees: {}>'.format(self.tree_entry, self.subtrees)
