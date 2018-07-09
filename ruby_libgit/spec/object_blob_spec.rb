require 'digest'
require 'fileutils'
require 'spec_helper'

describe RubyLibgit::ObjectBlob do
  before :each do
    @git_repo = '/tmp/objects-repo'
    @git_root_dir = ::File.join(@git_repo, '.git')
    @objects_dir = ::File.join(@git_root_dir, 'objects')

    repo = double('repo', :get_repo_root => @git_root_dir)
    FileUtils.mkdir_p(@objects_dir, mode: 0o644)
    ::Dir.chdir(@objects_dir)

    @obj = RubyLibgit::ObjectBlob.new(repo)
    @content = "hello world\n"
  end

  after :each do
    FileUtils.remove_dir(@git_repo, force=true)
  end

  it 'successfully stores blob on new blob hash' do
    content_hash = Digest::SHA1.hexdigest @content
    @obj.store_blob(content_hash, @content)

    filename = ::File.join(content_hash[0, 2], content_hash[2..-1])
    blob_file = ::File.exist?(::File.join(@objects_dir, filename))
    expect(blob_file).to be true
  end

  it 'raises exception when store blob on existing blob' do
    content_hash = Digest::SHA1.hexdigest @content

    allow(::File).to receive(:exist?) { true }
    expect { @obj.send :store_blob, content_hash, @content }.to raise_error(RubyLibgit::BlobHashConflictError)
  end
end
