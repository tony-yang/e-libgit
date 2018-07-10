require 'spec_helper'

describe RubyLibgit::Repo do
  subject(:repo) { described_class.new }
  before :each do
    ::Dir.chdir('/tmp')
    @repo_name = 'hello-git'
    @init = RubyLibgit::Init.new
    @init.create_git_repo(@repo_name)
    @git_repo = RubyLibgit::Repo.new
  end

  after :each do
    ::Dir.chdir('/tmp')
    FileUtils.remove_dir(@repo_name, force=true)
  end

  it 'returns true with good repo name' do
    repo_name = 'hello-git'
    good_name = repo.send :correct_naming_convention?, repo_name
    expect(good_name).to be true
  end

  it 'raises exception with invalid repo name' do
    repo_name = 'hello-git*'
    expect{ repo.send :correct_naming_convention?, repo_name }.to raise_error(RubyLibgit::FileNamingConventionError)
  end

  it 'raises exception with duplicate repo name' do
    repo_name = 'hello-git'
    allow(::Dir).to receive(:exist?) { true }
    expect{ repo.send :repo_exist?, repo_name }.to raise_error(RubyLibgit::RepositoryExistError)
  end

  it 'successfully finds the repo root when git at the current directory level' do
    full_path = ::File.join('/tmp', @repo_name)
    ::Dir.chdir(full_path)
    repo_root_dir = @git_repo.get_repo_root(full_path)
    expected_path = ::File.join(full_path, '.git')
    expect(repo_root_dir).to eq(expected_path)
  end

  it 'raises exception when not a git repo' do
    non_git_dir = '/tmp/non-repo'
    FileUtils.mkdir_p(non_git_dir)
    ::Dir.chdir(non_git_dir)

    expect{ repo.send :get_repo_root, non_git_dir }.to raise_error(RubyLibgit::NotGitRepoError)
  end
end
