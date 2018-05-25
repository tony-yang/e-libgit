all: build-container test-py-libgit test-ruby-libgit

build-container:
	docker build -t e-libgit .

test-py-libgit:
	docker run --rm e-libgit bash -c "cd py_libgit && make test"

test-ruby-libgit:
	docker run --rm e-libgit bash -c "cd ruby_libgit && rake"
