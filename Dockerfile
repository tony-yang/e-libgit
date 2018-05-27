# My personal dev env Docker image from my baremetal-init repo
FROM ubuntu-dev

RUN pip3 install --upgrade \
    coverage \
    pip \
    setuptools

RUN gem install \
    bundler \
    json \
    rake \
    rubocop \
    rspec \
    simplecov

ADD . /root/

RUN mkdir /var/log/py_libgit && mkdir /var/log/ruby_libgit

RUN pip install -e /root/py_libgit/. \
 && cd /root/ruby_libgit \
 && rake install
