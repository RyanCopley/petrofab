all: test
	test:
	nosetests --with-coverage --cover-package petrofab --cover-erase --with-doctest --nocapture
coverage: test
	coverage html
