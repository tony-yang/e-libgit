require 'fileutils'
require 'ruby_libgit'

module RubyLibgit
  # The Refs class
  class Refs
    def initialize
      RubyLibgit::Logging.logger.info('Create a Refs object')
      @pwd = ::Dir.pwd
    end

    def create_refs_dir(repo_name)
      refs_dir = ::File.join(@pwd, repo_name, '.git', 'refs', 'heads')
      FileUtils.mkdir_p(refs_dir, mode: 0o644)
    end
  end
end
