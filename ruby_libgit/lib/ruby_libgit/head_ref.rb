require 'ruby_libgit'

module RubyLibgit
  # The HEAD Ref class
  class HeadRef
    def initialize
      RubyLibgit::Logging.logger.info('Create a new HEAD Ref')
      @pwd = ::Dir.pwd
    end

    def create_head_ref_file(repo_name)
      head_file = ::File.join(@pwd, repo_name, '.git', 'HEAD')
      ::File.open(head_file, ::File::RDWR | ::File::CREAT, 0o644) do |f|
        f.write('ref: refs/heads/master')
      end
    end
  end
end
