SRC = $(wildcard nbs/*.ipynb)

all: let_me_answer_for_you docs

let_me_answer_for_you: $(SRC)
	nbdev_build_lib
	touch let_me_answer_for_you

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist