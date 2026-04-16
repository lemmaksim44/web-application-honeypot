# web-application-honeypot

## Развертывание приложения

### 1. Клонирование репозитория

```bash
git clone https://github.com/lemmaksim44/web-application-honeypot.git
```

### 2. Настройка переменных окружения

Отредактируйте файл `.env`, расположенный в директории:

```
app/.env
```

Необходимо указать:
 - секретный ключ Django
 - публичный и приватный ключи Google reCAPTCHA
 - публичный и приватный ключи Cloudflare Turnstile

### 3. Сборка Docker-образа

```bash
docker build -t honeypot .
```

### 4. Запуск контейнера

```bash
docker run -d -p 8000:8000 honeypot
```

## Доступ к приложению

После запуска приложение будет доступно по адресу:

[http://localhost:8000](http://localhost:8000)
