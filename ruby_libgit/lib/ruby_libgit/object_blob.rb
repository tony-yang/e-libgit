require 'digest'
require 'fileutils'
require 'ruby_libgit'

module RubyLibgit
  # The ObjectBlob class that represents individual object blob
  class ObjectBlob
    def initialize(repo)
      RubyLibgit::Logging.logger.info('Create a new Object object')
      @repo = repo
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
        match_dir = ::File.join(pathname, '**', '*')
        ::Dir.glob(match_dir, ::File::FNM_DOTMATCH) do |path|
          next if path.include? '.git'
          RubyLibgit::Logging.logger.info("Creating blob object for path = #{path}")
          content_hash = create_blob_object(path) if ::File.file?(path)
        end
      end
      content_hash
    end

    private

    def create_hash(content)
      RubyLibgit::Logging.logger.info("content = #{content}")
      content_hash = Digest::SHA1.hexdigest content
      RubyLibgit::Logging.logger.info("hash of content = #{content_hash}")
      content_hash
    end

    def store_blob(content_hash, content)
      RubyLibgit::Logging.logger.info("In dir = #{::Dir.pwd}")
      root_dir = @repo.get_repo_root(::Dir.pwd)
      object_dir = ::File.join(root_dir, 'objects', content_hash[0, 2])
      full_path = ::File.join(object_dir, content_hash[2..-1])
      if ::File.exist?(full_path)
        raise RubyLibgit::BlobHashConflictError, 'There is a conflict in blob hash. This will cause information loss.'
      else
        RubyLibgit::Logging.logger.info("Create a new blob hash wit hash = #{content_hash} at dir = #{object_dir}")
        FileUtils.mkdir_p(object_dir, mode: 0o644)
        RubyLibgit::Logging.logger.info("Creating object blob at = #{full_path}")
        ::File.open(full_path, 'w') do |f|
          f.write(content)
        end
      end
    end
  end
end
