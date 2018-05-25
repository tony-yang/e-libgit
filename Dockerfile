# My personal dev env Docker image from my baremetal-init repo
FROM ubuntu-dev

RUN pip3 install --upgrade \
    coverage \
    pip \
    setuptools

ADD . /root/

RUN mkdir /var/log/py_libgit
RUN pip install -e /root/py_libgit/.
