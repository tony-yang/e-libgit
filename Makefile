all: py-libgit

py-libgit:
	docker build -t e-libgit .
	docker run --rm e-libgit bash -c "cd py_libgit && make test"
