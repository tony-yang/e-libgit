# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'ruby_libgit/version'

Gem::Specification.new do |spec|
  spec.name          = "ruby_libgit"
  spec.version       = RubyLibgit::VERSION
  spec.authors       = ["Tony Yang"]
  spec.email         = ["tianyuyang658@yahoo.com"]

  spec.summary       = %q{Experimental Git implemented in Ruby}
  spec.description   = %q{Experimental Git implemented in Ruby}
  spec.homepage      = "https://github.com/tony-yang/e-libgit"

  # Prevent pushing this gem to RubyGems.org by setting 'allowed_push_host', or
  # delete this section to allow pushing this gem to any host.
  if spec.respond_to?(:metadata)
    spec.metadata['allowed_push_host'] = "TODO: Set to 'http://mygemserver.com'"
  else
    raise "RubyGems 2.0 or newer is required to protect against public gem pushes."
  end

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  spec.bindir        = "bin"
  spec.executables   = ["rbgit"]
  spec.require_paths = ["lib"]

  spec.add_development_dependency "bundler", "~> 1.11"
  spec.add_development_dependency "rake", "~> 10.0"
  spec.add_development_dependency "rubocop", "~> 0.56.0"
  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "simplecov", "~> 0.16"
end
