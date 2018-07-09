module RubyLibgit
  # File Naming Convention Exception
  class FileNamingConventionError < StandardError
    def initialize(msg = 'File name should only contain letters, digits, _, ., and -')
      super
    end
  end

  # Repository Exist Exception
  class RepositoryExistError < StandardError
    def initialize(msg = 'The git repository already exists!')
      super
    end
  end

  # Not a Git Repository Exception
  class NotGitRepoError < StandardError
    def initialize(msg = 'This is not a git repository')
      super
    end
  end

  # Blob Hash Conflict Exception
  class BlobHashConflictError < StandardError
    def initialize(msg = 'There is a conflict in blob hash. This will cause information loss')
      super
    end
  end
end
