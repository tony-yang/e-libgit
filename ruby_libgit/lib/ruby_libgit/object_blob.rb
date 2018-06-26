require 'ruby_libgit'

module RubyLibgit
  # The ObjectBlob class that represents individual object blob
  class ObjectBlob
    def initialize(repo)
      RubyLibgit::Logging.logger.info('Create a new Object object')
      @repo = repo
    end

    def create_hash(content)
      RubyLibgit::Logging.logger.info("content = #{content}")
      content_hash = '123'
      RubyLibgit::Logging.logger.info("hash of content = #{content_hash}")
      content_hash
    end

    def store_blob(content_hash, content)
      RubyLibgit::Logging.logger.info("In dir = #{::Dir.pwd}")
      #root_dir = @repo.get_repo_root(::Dir.pwd)
    end

    def create_blob_object(pathname)
      content_hash = nil
      if ::File.file?(pathname)
        ::File.open(pathname, 'r') do |f|
          content = f.read
          content_hash = create_hash(content)
          store_blob(content_hash, content)
        end
      elsif ::File.directory?(pathname)
        content_hash = '123'
      end
      content_hash
    end
  end
end
