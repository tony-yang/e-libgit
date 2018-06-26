require 'fileutils'
require 'ruby_libgit'

module RubyLibgit
  # The Objects class
  class Objects
    def initialize(repo)
      RubyLibgit::Logging.logger.info('Create an Objects object')
      @pwd = ::Dir.pwd
      @repo = repo
    end

    def create_objects_dir(repo_name, bare_repo = false)
      objects_dir = if bare_repo
                      ::File.join(@pwd, repo_name, 'objects')
                    else
                      ::File.join(@pwd, repo_name, '.git', 'objects')
                    end

      FileUtils.mkdir_p(objects_dir, mode: 0o644)
    end

    def create_object(pathname)
      pwd = ::Dir.pwd
      full_pathname = ::File.join(pwd, pathname)
      blob_object = RubyLibgit::ObjectBlob.new(@repo)
      blob_object.create_blob_object(full_pathname)
    end
  end
end
