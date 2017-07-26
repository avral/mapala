# Mapala

### Features

* Django backend in `./backend`
* vuejs (v2) frontend in `./frontend`
* Makefile to make your life easy

### Development environment setup

These steps will install all required dependencies including development ones, run migrations and start dev server.

```bash
make dev
make migrate
make run
```

### Deployment

These steps will install productio dependencies and build vuejs application to `static/dist` folder.

```bash
make prod
make build
```
