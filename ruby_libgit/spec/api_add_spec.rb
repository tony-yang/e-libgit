require 'spec_helper'
require 'fileutils'

describe RubyLibgit::Add do
  before :each do
    ::Dir.chdir('/tmp')
    @repo_name = 'hellogit-testrepo'
    @add = RubyLibgit::Add.new
    @init = RubyLibgit::Init.new
    @init.create_git_repo(@repo_name)

    @filename = 'hello'
    @pwd = ::Dir.pwd
    content = "hello world\n"

    ::Dir.chdir(::File.join(@pwd, @repo_name))
    open(@filename, 'w') do |f|
      f.puts content
    end
  end

  after :each do
    ::Dir.chdir('/tmp')
    FileUtils.remove_dir(@repo_name, force=true)
  end

  it 'successfully creates a blob and returns its hash' do
    content_hash = @add.create_blob(@filename)
    expect(content_hash).to eq('22596363b3de40b06f981fb85d82312e8c0ed511')

    object_blob_path = ::File.join(@pwd, @repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
    object_blob = ::File.exist?(object_blob_path)
    expect(object_blob).to be true
  end

  it 'successfully creates all blobs when passing shell wildcard to add' do
    shell_glob = '.'
    content_hash = @add.create_blob(shell_glob)
    expect(content_hash).to eq('22596363b3de40b06f981fb85d82312e8c0ed511')

    object_blob_path = ::File.join(@pwd, @repo_name, '.git', 'objects', '22', '596363b3de40b06f981fb85d82312e8c0ed511')
    object_blob = ::File.exist?(object_blob_path)
    expect(object_blob).to be true

    git_HEAD_blob_path = ::File.join(@pwd, @repo_name, '.git', 'objects', '7b', 'eb154244f8644b1f14114de8a1acc836d67e88')
    head_blob = ::File.exist?(git_HEAD_blob_path)
    expect(head_blob).to be false
  end
end
