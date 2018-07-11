require 'ruby_libgit'

module RubyLibgit
  # The Index tracking class that tracks all files in the repository
  class Index
    def initialize(repo)
      RubyLibgit::Logging.logger.info('Create a new Index object')
      @repo = repo
      @git_root = @repo.get_repo_root(::Dir.pwd)
      @index_file = ::File.join(@git_root, 'index')
    end

    def update_index(pathname)
      pathname = normalize_pathname(pathname)
      tracked_index = {}
      tracked_index = build_tracked_index if ::File.exist?(@index_file)

      unless tracked_index.key?(pathname)
        ::File.open(@index_file, 'a+') { |f| f.write("#{pathname}\n") }
        return true
      end

      false
    end

    private

    def build_tracked_index
      tracked_index = {}
      ::File.open(@index_file, 'r') do |files|
        files.each { |file| tracked_index[file.strip] = true }
      end
      tracked_index
    end

    def normalize_pathname(pathname)
      repo_name = @git_root.split('/')[-2]
      pathes = pathname.split('/')
      repo_name_index = 0
      pathes.each_with_index do |item, i|
        if item.eql?(repo_name)
          repo_name_index = i
          break
        end
      end
      reduced_pathes = []
      while repo_name_index < pathes.length
        item = pathes[repo_name_index]
        if item && item == '..'
          reduced_pathes.pop
        elsif item && item != '.'
          reduced_pathes.push item
        end
        repo_name_index += 1
      end
      ::File.join(reduced_pathes)
    end
  end
end
