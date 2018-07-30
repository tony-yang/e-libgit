import time

class CommitEntry:
    def __init__(self, message, author='author1', email='NO EMAIL', root_tree_sha1='', parents_sha1=[]):
        self.message = message
        self.root_tree_sha1 = root_tree_sha1
        self.parents_sha1 = parents_sha1
        self.author = author
        self.email = email
        self.timestamp = int(time.time())

    def __repr__(self):
        return 'Commit: <author: {} <{}> {} +0000, message: {}, tree: {}, parents: {}>'.format(self.author, self.email, self.timestamp, self.message, self.root_tree_sha1, self.parents_sha1)
