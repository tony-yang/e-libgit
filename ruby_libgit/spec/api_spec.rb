require 'spec_helper'
require 'fileutils'

describe RubyLibgit::Init do
  before :each do
    @repo_name = 'hellogit-testrepo'
    @init = RubyLibgit::Init.new(@repo_name)
  end

  after :each do
    FileUtils.remove_dir(@repo_name, force=true)
  end

  it 'successfully creates a git repo with valid name' do
    @init.create_git_repo

    pwd = ::Dir.pwd
    repo_path = ::File.join(pwd, @repo_name, '.git')
    repo_dir = ::Dir.exist?(repo_path)

    objects_path = ::File.join(pwd, @repo_name, '.git', 'objects')
    objects_dir = ::Dir.exist?(objects_path)

    refs_path = ::File.join(pwd, @repo_name, '.git', 'refs', 'heads')
    refs_dir = ::Dir.exist?(refs_path)

    head_path = ::File.join(pwd, @repo_name, '.git', 'HEAD')
    head_file = ::File.exist?(head_path)

    expect(repo_dir).to be true
    expect(objects_dir).to be true
    expect(refs_dir).to be true
    expect(head_file).to be true
  end

  it 'should raise an exception when creating a repo with invalid name' do
    repo_name = 'hellogit*'
    init = RubyLibgit::Init.new(repo_name)
    expect{ init.create_git_repo }.to raise_error(RubyLibgit::FileNamingConventionError)
  end
end
