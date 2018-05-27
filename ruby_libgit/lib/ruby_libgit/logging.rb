require 'logger'

module RubyLibgit
  # Module level Logger shared by all instances
  module Logging
    def self.logger
      defined?(@logger) ? @logger : initialize_logger
      RubyLibgit::Logging
    end

    def self.initialize_logger
      log_file = '/var/log/ruby_libgit/app.log'
      @logger = Logger.new(log_file, 10, 512_000)
    end

    def self.info(message)
      filename = caller(1..1).first.split(':')
      filename[0] = ::File.basename(filename[0])
      filename = filename.join(':')
      @logger.info(filename) { message }
    end
  end
end
