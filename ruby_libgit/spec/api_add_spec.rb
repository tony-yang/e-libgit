require 'spec_helper'
require 'fileutils'

describe RubyLibgit::Add do
  before :each do
    ::Dir.chdir('/tmp')
    @repo_name = 'hellogit-testrepo'
    @add = RubyLibgit::Add.new
    @init = RubyLibgit::Init.new
    @init.create_git_repo(@repo_name)
  end

  after :each do
    ::Dir.chdir('/tmp')
    FileUtils.remove_dir(@repo_name, force=true)
  end

  it 'successfully creates a blob and returns its hash' do
    filename = 'hello'
    content = "hello world\n"
    pwd = ::Dir.pwd

    ::Dir.chdir(::File.join(pwd, @repo_name))
    open(filename, 'w') do |f|
      f.puts content
    end

    content_hash = @add.create_blob(filename)
    expect(content_hash).to eq('123')
  end
end
