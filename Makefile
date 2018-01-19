install:
	python setup.py install

clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -f .coverage
	rm -rf build
	rm -rf dist
	rm -rf damnboleto.egg-info

test: clean
	nosetests -s --rednose

coverage: clean
	nosetests --with-coverage --cover-package=damnboleto

bandit: clean
	bandit -r damnboleto
