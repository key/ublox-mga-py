init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run coverage run setup.py test

codecov:
	pipenv run codecov --token=${CODECOV_UPLOAD_TOKEN}
