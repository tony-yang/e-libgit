module RubyLibgit
  # File Naming Convention Exception
  class FileNamingConventionError < StandardError
    def initialize(msg = 'File name should only contain letters, digits, _, ., and -')
      super
    end
  end
end
