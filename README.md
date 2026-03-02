# Map of Location Popularity

Веб-додаток (Django REST Framework) для перегляду та оцінки популярних локацій з інтерактивною рейтинговою системою та аналітикою.

## 🚀 Швидкий старт (Docker) - Рекомендовано

1. **Клонуйте репозиторій:**
   ```bash
   git clone <repository-url>
   cd map-of-location-popularity
   ```

2. **Створіть `.env` файл:**
   ```bash
   cp .env.example .env
   # Переконайтесь, що змінні підходять (DB_HOST=db, REDIS_URL=redis://redis:6379/1)
   ```

3. **Запустіть проект:**
   ```bash
   docker-compose up --build
   ```

4. **Застосуйте міграції (в іншому терміналі):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

Додаток доступний за адресою: `http://localhost:8000/api/`

---

## 🛠 Локальний запуск (без Docker)

Вимоги: Python 3.10+, PostgreSQL, Redis.

1. **Створіть віртуальне середовище:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Налаштуйте `.env`:**
   Вкажіть локальні `DB_HOST=localhost`, `DB_PORT=5432` та `REDIS_URL`.

4. **Запустіть міграції:**
   ```bash
   python manage.py migrate
   ```

5. **Запустіть сервер:**
   ```bash
   python manage.py runserver
   ```

---

## 📚 Основний стек
- **Backend:** Django, DRF
- **Database:** PostgreSQL
- **Cache:** Redis
- **Data Export:** Pandas
