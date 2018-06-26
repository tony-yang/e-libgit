require 'ruby_libgit'

module RubyLibgit
  # The Git init API class
  class Init
    def initialize
      RubyLibgit::Logging.logger.info('Create the Init object')
    end

    # Create a new git repository
    # Params:
    # - repo_name: the name of the repository
    # - bare_repo: specify if this is a bare repo (default false)
    def create_git_repo(repo_name, bare_repo = false)
      @repo_name = repo_name
      @repo = RubyLibgit::Repo.new
      begin
        @repo.create_repo(@repo_name, bare_repo)
      rescue RubyLibgit::RepositoryExistError => error
        RubyLibgit::Logging.logger.info(error)
        warn error
      end
    end
  end

  # The Git add API class
  class Add
    def initialize
      RubyLibgit::Logging.logger.info('Create the Add object')
      @repo = RubyLibgit::Repo.new
      @objects = RubyLibgit::Objects.new(@repo)
    end

    # Create a new blob under the object directory that saves the actual file content
    # Params:
    # - pathname: the name of the file to be added into the repo
    def create_blob(pathname)
      @pathname = pathname
      @objects.create_object(@pathname)
    end
  end
end
