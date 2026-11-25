# project_de_el_v2
Second version of the project for loading data from an API into PostgreSQL, with the addition of a Dockerfile and a docker-compose.yaml file

# Data Pipeline v2: JSONPlaceholder → CSV → PostgreSQL

Скрипт забирает данные из JSONPlaceholder, сохраняет их в CSV, читает обратно и загружает в PostgreSQL. Повторный запуск безопасен: дубли не создаются благодаря `ON CONFLICT (id) DO NOTHING`.

**Версия 2** — рефакторинг архитектуры v1: единая точка входа `main.py`, функции вместо скриптов, подготовка к контейнеризации (Docker).

## Задачи

- Сбор данных из API
- Получение списка словарей из ответа API
- Преобразование в DataFrame
- Сохранение DataFrame в CSV-файл
- Чтение файла и загрузка данных из CSV в список кортежей
- Подключение к БД PostgreSQL
- Создание таблицы
- Загрузка данных в таблицу

## Структура проекта
```
.
├── main.py # точка входа: extract → save_to_csv → read_csv → load
├── extract.py # получение данных из API и сохранение в CSV
├── read_csv.py # чтение CSV и преобразование в список кортежей
├── load_to_db.py # подключение к PostgreSQL, создание таблицы, вставка
├── .env.example # шаблон переменных окружения (без секретов)
├── .gitignore # исключает .env, venv, данные
├── requirements.txt # зависимости проекта
└── README.md
```
## Изменения по сравнению с v1

- **Единая точка входа** — `main.py`. Запуск одним файлом: `python main.py`.
- **`load.py` → `load_to_db.py`**, логика загрузки обёрнута в функцию `load(values)`. При импорте ничего не выполняется — загрузка запускается только явным вызовом из `main.py`.
- **Путь к CSV** резолвится через `Path(__file__).resolve().parent` — файл всегда ищется рядом со скриптами, независимо от текущей рабочей директории.
- **`save_to_csv()`** возвращает результат через печать в консоль (без `bool`), проверка на пустой DataFrame остаётся внутри функции.
- **Разделение ответственности**: `extract` — получает данные, `read_csv` — читает CSV, `load` — заливает в БД, `main` — связывает их по порядку.

## Установка и запуск

1. Клонировать репозиторий:
```bash
   git clone <url-репозитория>
   cd <папка-проекта>
```
2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```
3. Установить зависимости:

```bash
pip install -r requirements.txt
Создать .env на основе .env.example и заполнить своими параметрами:
```
```bash
cp .env.example .env
```
4. Затем откройте .env и укажите:

```text
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
5. Убедитесь, что у вас уже создана база данных.

6. Запустить скрипт:

```bash
python main.py
```
## Результат
Таблица raw_data со схемой:

| Колонка  | Тип     | Ограничение |
|----------|---------|-------------|
| "userId" | INTEGER |             |
| id       | INTEGER | PRIMARY KEY |
| title    | TEXT    |             |
| body     | TEXT    |             |	


Скрипт загружает данные в таблицу raw_data. Проверено: после первого запуска в таблице 100 строк, после повторного — те же 100 без дублей.

## Пример вывода:

```text
data saved successfully in the /путь/к/проекту/extract_to_csv.csv
Прочитано строк из CSV: 100
Всего строк в таблице: 100
```

## Используемые библиотеки
requests, pandas, psycopg2-binary, python-dotenv

## Функции
1) extract() — получает данные из API и преобразует в DataFrame
2) save_to_csv() — сохраняет DataFrame в CSV-файл
3) read_csv_to_tuples() — считывает CSV-файл и сохраняет кортежи в список
4) load(values) — подключается к PostgreSQL, создаёт таблицу и вставляет данные
5) main_launch() — оркестратор: вызывает функции пайплайна по порядку

## Лицензия
MIT

