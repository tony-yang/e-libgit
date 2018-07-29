import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os
from py_libgit.core.commit_blob import CommitBlob
from py_libgit.core.commit_entry import CommitEntry
from py_libgit.core.commit_tree import CommitTree
from py_libgit.core.index_entry import IndexEntry
from py_libgit.core.object_blob import ObjectBlob
from py_libgit.core.tree_entry import TreeEntry, EntryType

class Objects:
    def __init__(self, repo, index):
        logger.info('Create an Objects object')
        self.pwd = os.getcwd()
        self.repo = repo
        self.index = index

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

        staging_content = []
        tracked_index = self.index.build_tracked_index()

        if os.path.isfile(full_pathname):
            content_hash = blob_object.create_blob_object(full_pathname)
            current_sha1 = '0'*40
            normalized_path = self.index.normalize_pathname(full_pathname)
            if normalized_path in tracked_index:
                current_sha1 = tracked_index[normalized_path].current_sha1
            staging_content.append(IndexEntry(full_pathname, current_sha1=current_sha1, new_sha1=content_hash))
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
                    current_sha1 = '0'*40
                    normalized_path = self.index.normalize_pathname(full_pathname)
                    if normalized_path in tracked_index:
                        current_sha1 = tracked_index[normalized_path].current_sha1
                    staging_content.append(IndexEntry(full_pathname, current_sha1=current_sha1, new_sha1=content_hash))
        else:
            return None

        self.index.update_index(staging_content)
        return content_hash

    def create_cached_tree_objects(self):
        index_content = []
        tracked_index = self.index.build_tracked_index()
        git_root_name = self.repo.get_repo_root(os.getcwd()).split('/')[-2]
        root = CommitTree(self.repo, TreeEntry(git_root_name, entry_type=EntryType.TREE))
        commit_trees = {git_root_name: root}
        for pathname, attributes in tracked_index.items():
            pathname_structure = pathname.split('/')
            for i, item in enumerate(pathname_structure):
                if item not in commit_trees:
                    if i < len(pathname_structure)-1:
                        subtree = CommitTree(self.repo, TreeEntry(item, entry_type=EntryType.TREE, sha1=attributes.new_sha1))
                    else:
                        subtree = CommitTree(self.repo, TreeEntry(item, entry_type=EntryType.BLOB, sha1=attributes.new_sha1))
                        index_content.append(IndexEntry(pathname, current_sha1=attributes.new_sha1, new_sha1=attributes.new_sha1))
                    commit_trees[item] = subtree
                    parent_tree = commit_trees[pathname_structure[i-1]]
                    parent_tree.add_subtree(subtree)
        root_tree_entry = root.commit_tree_blob()
        logger.info('The root tree entry = {}'.format(root_tree_entry))
        self.index.update_index(index_content)
        return root_tree_entry

    def create_commit(self, author, message, root_tree_entry):
        commit_entry = CommitEntry(message=message, author=author, root_tree_sha1 = root_tree_entry.sha1)
        commit_blob = CommitBlob(self.repo)
        commit_hash = commit_blob.create_commit(commit_entry)
        return commit_hash
