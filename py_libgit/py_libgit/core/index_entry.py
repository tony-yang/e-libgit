import logging, py_libgit.settings
logger = logging.getLogger(__name__)

class IndexEntry:
    def __init__(self, pathname, current_sha1='0'*40, new_sha1='0'*40, unix_mode='10000644'):
        logger.info('Create an Index object')
        self.pathname = pathname
        self.current_sha1 = current_sha1
        self.new_sha1 = new_sha1
        self.unix_mode = unix_mode
