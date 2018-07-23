from enum import Enum

class EntryType(Enum):
    BLOB = 1
    TREE = 2
    COMMIT = 3

class TreeEntry:
    def __init__(self, name, unix_mode='10000644', entry_type=EntryType.BLOB, sha1='0'*40):
        self.name = name
        self.unix_mode = unix_mode
        self.entry_type = entry_type
        self.sha1 = sha1

    def __repr__(self):
        return 'Tree Entry: <name: {}, unix_mode: {}, entry_type: {}, sha1: {}>'.format(self.name, self.unix_mode, self.entry_type, self.sha1)
