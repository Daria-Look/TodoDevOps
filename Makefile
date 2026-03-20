DC = docker-compose

# Docker: Запуск всего проекта с пересборкой
# добавляем ключевые слова frontend и backend в конце команды, если нужно сделать точечную пересборку
up:
	$(DC) up --build -d

# Docker: Остановка всего проекта
down:
	$(DC) down

# Docker: Запуск тестов бэкенда
test-back:
	$(DC) exec backend pytest test_main.py

# Docker: Запуск тестов фронтенда
test-front:
	$(DC) exec frontend npm test

# Docker: Полная проверка
test-all: down up test-back test-front

# Docker: Посмотреть логи бэкенда
logs-back:
	$(DC) logs -f backend

.PHONY: up down test-back test-front test-all logs-back