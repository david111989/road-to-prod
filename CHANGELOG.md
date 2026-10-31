# Changelog

Формат: [Keep a Changelog](https://keepachangelog.com/), версии по [SemVer](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-10-31
### Added
- Сервис гостевой книги на FastAPI: `/health`, `GET /entries`, `POST /entries`
- Хранение записей в PostgreSQL
- Dockerfile, compose.yaml с healthcheck и volume
- CI (Ruff, pytest) и публикация образа в ghcr.io
