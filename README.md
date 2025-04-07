# JSON Validator Service

[![CI/CD Pipeline](https://github.com/gireassen/json_validator/actions/workflows/docker-build-test.yml/badge.svg)](https://github.com/gireassen/json_validator/actions/workflows/docker-build-test.yml)
[![Last Commit](https://img.shields.io/github/last-commit/gireassen/json_validator)](https://github.com/gireassen/json_validator/commits/main)
[![Docker Pulls](https://img.shields.io/docker/pulls/gias123/json_validator)](https://hub.docker.com/r/gias123/json_validator)
[![Docker Image Size](https://img.shields.io/docker/image-size/gias123/json_validator/latest)](https://hub.docker.com/r/gias123/json_validator)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/)
[![GitHub License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/gireassen/json_validator/blob/main/LICENSE)


Простое веб-приложение для валидации JSON.

## Запуск с Docker

```bash
docker build -t json-validator .
docker run -p 8000:8000 json-validator
```

## Запуск с DockerHub
```bash
docker run -p 8000:8000 gias123/json_validator:latest
```

Приложение будет доступно по адресу: http://localhost:8000