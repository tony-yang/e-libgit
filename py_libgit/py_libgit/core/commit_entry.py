class CommitEntry:
    def __init__(self, message, author='author1', root_tree_sha1='', parents_sha1=[]):
        self.message = message
        self.root_tree_sha1 = root_tree_sha1
        self.parents_sha1 = parents_sha1
        self.author = author

    def __repr__(self):
        return 'Commit: <author: {}, message: {}, tree: {}, parents: {}>'.format(self.author, self.message, self.root_tree_sha1, self.parents_sha1)
