module RubyLibgit
  # File Naming Convention Exception
  class FileNamingConventionError < StandardError
    def initialize(msg = 'File name should only contain letters, digits, _, ., and -')
      super
    end
  end

  # Repository Exist Exception Exception
  class RepositoryExistError < StandardError
    def initialize(msg = 'The git repository already exists!')
      super
    end
  end
end
