# JSON Validator Service

[![CI/CD Pipeline](https://github.com/gireassen/json_validator/actions/workflows/docker-build-test.yml/badge.svg)](https://github.com/gireassen/json_validator/actions/workflows/docker-build-test.yml)

[![Docker Image Version](https://img.shields.io/docker/v/gireassen/json_validator?sort=semver)](https://hub.docker.com/r/gireassen/json_validator)

[![Docker Pulls](https://img.shields.io/docker/pulls/gireassen/json_validator)](https://hub.docker.com/r/gireassen/json_validator)

[![Docker Image Size](https://img.shields.io/docker/image-size/gireassen/json_validator/latest)](https://hub.docker.com/r/gireassen/json_validator)

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/)

[![License](https://img.shields.io/github/license/gireassen/json_validator)](https://github.com/gireassen/json_validator/blob/main/LICENSE)

Простое веб-приложение для валидации JSON.

## Запуск с Docker

```bash
docker build -t json-validator .
docker run -p 8000:8000 json-validator
```

## Запуск с DockerHub
```bash
docker run -p 8000:8000 gireassen/json_validator:latest
```

Приложение будет доступно по адресу: http://localhost:8000