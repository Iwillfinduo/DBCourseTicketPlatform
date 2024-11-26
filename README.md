
# Курсовая работа
## Сервис управления заявками об ошибках
*-----english text below-----*
MVP - без деления на роли со стороны сервера,  
полной развертки в докер контейнерах и с так себе архитектурой.  

### Запуск

#### Развертывание базы данных PostgreSQL с PGAdmin (требуется Docker)
```
docker-compose up
```

#### Запуск Flask-сервера
Установка всех требуемых библиотек
```
pip install -r requirements.txt
```
Запуск сервера  (требуется задать переменные окружения: DB_HOST, DB_NAME,  
DB_PASSWORD, DB_PORT, DB_USER, SECRET_KEY)
```
python app.py
```

# DB Course Work
## bug ticket management service
MVP - without role differences, full docker deployment,  
and with fuzzy architecture
### Setting Up and Running

#### Deploying PostgreSQL DB with PGAdmin(requires Docker)
```
docker-compose up
```

#### Setting up Flask server
Installing all required libraries
```
pip install -r requirements.txt
```
Starting the server (you need to set the environment variables: DB_HOST,  
DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, SECRET_KEY)
```
python app.py
```


