require 'spec_helper'

describe RubyLibgit::Repo do
  subject(:repo) { described_class.new }

  it 'returns true with good repo name' do
    repo_name = 'hello-git'
    good_name = repo.send :correct_naming_convention?, repo_name
    expect(good_name).to be true
  end

  it 'raises exception with invalid repo name' do
    repo_name = 'hello-git*'
    expect{ repo.send :correct_naming_convention?, repo_name }.to raise_error(RubyLibgit::FileNamingConventionError)
  end
end
