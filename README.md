# Real-time чат с WebSocket

## Описание
Чат-приложение на Django с поддержкой WebSocket для обмена сообщениями в реальном времени.

## Стек технологий

- **Backend:** Python, Django
- **WebSocket:** Django Channels
- **Кеширование и управление состоянием:** Redis
- **Фоновые задачи:** Celery
- **База данных:** PostgreSQL
## Установка и запуск с Docker Compose

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/marina-serg/new-chat.git
cd new-chat
```

### 2. Создайте файл .env из шаблона
```bash
cp .env.template .env
```
### 3.Выполните сборку образов и запустите контейнеры:
```bash
docker compose build

docker compose up -d
```

### 4.После запуска контейнеров выполните миграции :
```bash
docker compose exec web python manage.py migrate --noinput


```
### 5.Доступ к приложению
После запуска контейнеров, откройте приложение в браузере по адресу http://127.0.0.1:8000/


