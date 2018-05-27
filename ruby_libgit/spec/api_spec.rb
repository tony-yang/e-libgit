require 'spec_helper'
require 'fileutils'

describe RubyLibgit::Init do
  before :each do
    @repo_name = 'hellogit-testrepo'
    @init = RubyLibgit::Init.new()
  end

  after :each do
    FileUtils.remove_dir(@repo_name, force=true)
  end

  it 'successfully creates a git repo with valid name' do
    @init.create_git_repo(@repo_name)

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
    init = RubyLibgit::Init.new
    expect{ init.create_git_repo(repo_name) }.to raise_error(RubyLibgit::FileNamingConventionError)
  end

  it 'successfully creates a bare git repo with valid name' do
    @init.create_git_repo(@repo_name, bare_repo=true)

    pwd = ::Dir.pwd
    objects_path = ::File.join(pwd, @repo_name, 'objects')
    objects_dir = ::Dir.exist?(objects_path)

    refs_path = ::File.join(pwd, @repo_name, 'refs', 'heads')
    refs_dir = ::Dir.exist?(refs_path)

    head_path = ::File.join(pwd, @repo_name, 'HEAD')
    head_file = ::File.exist?(head_path)

    expect(objects_dir).to be true
    expect(refs_dir).to be true
    expect(head_file).to be true
  end
end
