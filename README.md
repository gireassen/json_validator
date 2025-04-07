# JSON Validator Service

![Docker Build and Test](https://github.com/gireassen/json_validator/actions/workflows/docker-build-test.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/github/license/gireassen/json_validator)

Простое веб-приложение для валидации JSON.

## Запуск с Docker

```bash
docker build -t json-validator .
docker run -p 8000:8000 json-validator
```

Приложение будет доступно по адресу: http://localhost:8000