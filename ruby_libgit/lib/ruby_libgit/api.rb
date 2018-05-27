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
end
