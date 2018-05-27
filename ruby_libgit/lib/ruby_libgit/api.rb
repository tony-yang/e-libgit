require 'ruby_libgit'

module RubyLibgit
  # API
  class Init
    def initialize(repo_name)
      RubyLibgit::Logging.logger.info('Create the Init object')
      @repo_name = repo_name
    end

    def create_git_repo
      @repo = RubyLibgit::Repo.new
      @repo.create_repo(@repo_name)
    end
  end
end
