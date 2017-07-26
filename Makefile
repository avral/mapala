# Use development settings for running django dev server.
export DJANGO_SETTINGS_MODULE=backend.settings

# Initializes virtual environment with basic requirements.
prod:
	pip install -r requirements.txt
	npm install --production

# Installs development requirements.
dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	npm install

front-dev:
	npm run dev

back-dev:
	npm run dev & ./manage runserver

migrate:
	python ./manage makemigrations
	python ./manage migrate

build: prod migrate
	npm run build

# Cleans up folder by removing virtual environment, node modules and generated files.
clean:
	rm -rf node_modules
	rm -rf static/dist

# Run linter
lint:
	@npm run lint --silent


# это задание я дописал сам для рестарта ювсдж
reload:
	sudo fuser -k 80/tcp
	sudo fuser -k 8000/tcp
	uwsgi /srv/sites/mapala/proj/mapala/backend/uwsgi/uwsgi.ini #// это на самом деле надо
	sudo service nginx restart
