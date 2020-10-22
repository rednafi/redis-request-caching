lint:
	black . && isort .

update_deps:
	pip-compile --upgrade requirements.in

revert_deps:
	git checkout requirements.txt
