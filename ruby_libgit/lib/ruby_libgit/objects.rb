require 'fileutils'
require 'ruby_libgit'

module RubyLibgit
  # The Objects class
  class Objects
    def initialize
      RubyLibgit::Logging.logger.info('Create an Objects object')
      @pwd = ::Dir.pwd
    end

    def create_objects_dir(repo_name, bare_repo = false)
      objects_dir = if bare_repo
                      ::File.join(@pwd, repo_name, 'objects')
                    else
                      ::File.join(@pwd, repo_name, '.git', 'objects')
                    end

      FileUtils.mkdir_p(objects_dir, mode: 0o644)
    end
  end
end
