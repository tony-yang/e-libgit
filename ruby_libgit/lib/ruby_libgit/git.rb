require 'singleton'

require 'ruby_libgit'

module RubyLibgit
  # The Git CLI, program entry point referenced from the bin/rbgit
  class Git
    include Singleton

    def initialize
      p 'Create a new Git instance'
      RubyLibgit::Logging.logger.info('Create a new Git instance')
      @init = RubyLibgit::Init.new('testrepo')
    end

    def parse
      p 'Parse argument'
    end

    def run
      p 'Git run'
    end
  end
end
