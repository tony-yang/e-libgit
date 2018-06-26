require 'fileutils'
require 'ruby_libgit'

module RubyLibgit
  # The Git Repo class
  class Repo
    def initialize
      RubyLibgit::Logging.logger.info('Create a new Repo')
      @pwd = ::Dir.pwd
      @objects = RubyLibgit::Objects.new(self)
      @refs = RubyLibgit::Refs.new
      @head_ref = RubyLibgit::HeadRef.new
    end

    def create_repo(repo_name, bare_repo = false)
      correct_naming_convention?(repo_name)
      repo_exist?(repo_name)
      unless bare_repo
        git_repo = ::File.join(@pwd, repo_name, '.git')
        FileUtils.mkdir_p(git_repo, mode: 0o644)
      end

      @objects.create_objects_dir(repo_name, bare_repo)
      @refs.create_refs_dir(repo_name, bare_repo)
      @head_ref.create_head_ref_file(repo_name, bare_repo)
    end

    private

    def correct_naming_convention?(repo_name)
      if /[^a-zA-Z0-9_.-]/ =~ repo_name
        raise RubyLibgit::FileNamingConventionError, 'File name should only contain letters, digits, _, ., and -'
      end
      true
    end

    def repo_exist?(repo_name)
      if ::Dir.exist?(::File.join(@pwd, repo_name))
        raise RubyLibgit::RepositoryExistError, "The git repository #{repo_name} already exists!"
      end
      false
    end
  end
end
