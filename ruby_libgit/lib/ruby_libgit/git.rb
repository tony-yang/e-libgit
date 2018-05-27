require 'optparse'
require 'singleton'

require 'ruby_libgit'

module RubyLibgit
  # The Git CLI, program entry point referenced from the bin/rbgit
  class Git
    include Singleton

    def initialize
      RubyLibgit::Logging.logger.info('Create a new Git instance')
      @options = parse(ARGV)
    end

    # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity, Metrics/MethodLength
    def parse(args = ARGV)
      options = {}

      subcommands = {
        init: OptionParser.new do |o|
          o.banner = 'usage: git init <repo_name> [<args>] - Create an empty Git repository'
          options[:init] = {}
        end
      }

      parser = OptionParser.new do |o|
        o.banner = "usage: git <command> [<args>]\n\n"
        subcommands.each do |subcommand, subparser|
          o.banner += "Command\n\t" + subcommand.to_s
          o.banner += "\t\t" + subparser.help
        end

        o.on_tail('-h', '--help', 'List available subcommands and some concept guides.') do
          puts o
          exit
        end
      end

      if args[0] && subcommands.key?(args[0].to_sym)
        subcommand = args.shift.to_sym
        if args.empty?
          puts subcommands[subcommand].help
          exit
        else
          begin
            subcommands[subcommand].order! do |non_option_arg|
              options[subcommand][:non_option_arg] = non_option_arg
            end
          rescue OptionParser::ParseError => error
            warn error
            puts subcommands[subcommand].help
            exit 1
          end
        end
      elsif args.empty?
        puts parser.help
        exit
      else
        begin
          parser.parse!(args)
        rescue OptionParser::ParseError => error
          warn error
          puts parser.help
          exit 1
        end
      end
      options
    end
    # rubocop:enable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity, Metrics/MethodLength

    def run
      if @options.key?(:init)
        RubyLibgit::Logging.logger.info('Called with init repo_name ' + @options[:init][:non_option_arg])
        init = RubyLibgit::Init.new(@options[:init][:non_option_arg])
        init.create_git_repo
      end
    end
  end
end
