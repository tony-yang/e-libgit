require 'fileutils'
require 'spec_helper'

describe RubyLibgit::Index do
  before :each do
    @repo_name = 'repotest'
    @repo_dir = ::File.join('/tmp', @repo_name)
    @git_repo_root = ::File.join(@repo_dir, '.git')
    FileUtils.mkdir_p(@git_repo_root)

    repo = double('repo', :get_repo_root => @git_repo_root)

    @index = RubyLibgit::Index.new(repo)
    @index_file = ::File.join(@git_repo_root, 'index')
  end

  after :each do
    FileUtils.remove_dir(@repo_dir, force=true)
  end

  it 'should remove single dot path in normalize_pathname' do
    pathname = ::File.join(@repo_dir, 'abc/./test')
    normalized_pathname = @index.send :normalize_pathname, pathname
    expected_pathname = ::File.join(@repo_name, 'abc/test')
    expect(normalized_pathname).to eq(expected_pathname)
  end

  it 'should remove double dots with same path in normalize_pathname' do
    pathname = ::File.join(@repo_dir, 'abc/test/../test')
    normalized_pathname = @index.send :normalize_pathname, pathname
    expected_pathname = ::File.join(@repo_name, 'abc/test')
    expect(normalized_pathname).to eq(expected_pathname)
  end

  it 'should remove double dots with different path in normalize_pathname' do
    pathname = ::File.join(@repo_dir, 'abc/test1/../test2')
    normalized_pathname = @index.send :normalize_pathname, pathname
    expected_pathname = ::File.join(@repo_name, 'abc/test2')
    expect(normalized_pathname).to eq(expected_pathname)
  end

  it 'should remove multiple double dots path in normalize_pathname' do
    pathname = ::File.join(@repo_dir, 'abc/test1/test2/../../test3')
    normalized_pathname = @index.send :normalize_pathname, pathname
    expected_pathname = ::File.join(@repo_name, 'abc/test3')
    expect(normalized_pathname).to eq(expected_pathname)
  end

  it 'should remove multiple dots in separate locations in normalize_pathname' do
    pathname = ::File.join(@repo_dir, 'abc/test1/../test2/../test3')
    normalized_pathname = @index.send :normalize_pathname, pathname
    expected_pathname = ::File.join(@repo_name, 'abc/test3')
    expect(normalized_pathname).to eq(expected_pathname)
  end

  it 'successfully update index when no existing entry' do
    pathname = 'helloworld'
    @index.update_index(pathname)
    expect(::File.exist?(@index_file)).to be true

    index_content = nil
    ::File.open(@index_file, 'r') { |f| index_content = f.read() }
    expected_index_content = "#{pathname}\n"
    expect(index_content).to eq(expected_index_content)
  end

  it 'should not update index with duplicate entry' do
    pathname = 'helloworld'
    @index.update_index(pathname)
    @index.update_index(pathname)
    expect(::File.exist?(@index_file)).to be true

    index_content = nil
    ::File.open(@index_file, 'r') { |f| index_content = f.read() }
    expected_index_content = "#{pathname}\n"
    expect(index_content).to eq(expected_index_content)
  end

  it 'successfully updates two different entries into index' do
    pathname1 = 'helloworld'
    pathname2 = 'helloworld2'
    @index.update_index(pathname1)
    @index.update_index(pathname2)
    expect(::File.exist?(@index_file)).to be true

    index_content = nil
    ::File.open(@index_file, 'r') { |f| index_content = f.read() }
    expected_index_content = "#{pathname1}\n#{pathname2}\n"
    expect(index_content).to eq(expected_index_content)
  end
end
