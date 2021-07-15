# xsolla-backend-2021-test

Test for Xsolla School 2021. Backend: RESTful API for e-commerce game developer's system.

https://xsolla-backend-2021-test.herokuapp.com/

https://xsolla-backend-2021-test.herokuapp.com/swagger

https://xsolla-backend-2021-test.herokuapp.com/products

**Задача**: реализация системы управления товарами для площадки электронной коммерции (продажа таких товаров, как игры, мерч, виртуальная валюта и др.)

## Обязательная часть

Реализовать методы API для операций CRUD по управлению товарами. Товар определяется уникальным идентификатором и обязательно должен иметь [SKU](https://ru.wikipedia.org/wiki/SKU), имя, тип, стоимость. Для создания API используется библиотека [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/index.html).

1. **Создание товара**. Метод генерирует и возвращает уникальный идентификатор товара.
2. **Редактирование товара**. Метод изменяет все данные о товаре по его идентификатору или SKU.
3. **Удаление товара по его идентификатору или SKU**.
4. **Получение информации о товаре по его идентификатору или SKU**.
5. **Получение каталога товаров**. Метод возвращает список всех добавленных товаров по частям. В запросе нужно указать номер запрашиваемой страницы и максимальное количество записей на одну страницу.
6. **README** содержит краткое описание приложения и команды для разворачивания и тестирования.

## Дополнительная часть - доработка системы управления товарами

1. Информация о товарах хранится в базе данных mongodb, для работы с которой используется отображение объектов в документы (ODM) [MongoEngine](http://mongoengine.org/).
2. Создан скрипт `prepare_mongo.py`, который наполняет СУБД тестовыми данными из набора `test_dataset.json`.
3. Созданы модульные тесты `utest_api_resources.py`
4. Добавлена фильтрация товаров по их типу в **Методе получения каталога товаров**.
5. Составлена спецификация OpenAPI 3.0 в `./app/static/openapi.yaml`.
6. Созданы Dockerfile для создания образа с flask-приложением и Docker-compose файл для развертывания приложения.
7. База данны `mongodb` разворачивается в облаке или локально. Если определена переменная окружения `MONGO_PASSWD`, то приложение подключается к облачной базе данны `Atlas MongoDB`, иначе - локально.
8. Приложение развернуто на [`heroku`](https://xsolla-backend-2021-test.herokuapp.com/). Настроен автоматический деплой приложения на heroku после коммита в ветку heroku гитхаба.

## Способ тестирования приложения

Для локального развертывания приложения с помощью `docker-compose` необходимо выполнить команды:  

```bash
git clone https://github.com/konstgav/xsolla-backend-2021-test.git
cd xsolla-backend-2021-test
docker-compose up 
```

Описание спецификации OpenAPI 3.0 доступно по ссылке

```bash
http://localhost:5000/swagger/
```

Для тестирования используются пакеты `pymongo`, `requests`, `unittest`. Для запуска автотестов выполните команды:

```bash
pip3 install pymongo 
pip3 install requests
cd app
python3 -m unittest -v utest_api_resources.py
```

Автотесты содержат следующие запросы к приложению. Можно провести тестирование в ручном режиме при помощи следующих команд:

1. **Создание товара**

```bash
curl http://localhost:5000/products -d "name=gun" -d "sku=g8" -d "type=item" -d "price=3" -X POST
```

2. **Редактирование товара**

```bash
curl http://localhost:5000/product/1 -d "name=lucky coin" -d "price=9" -X PUT
```

3. **Удаление товара по его идентификатору** 

```bash
curl http://localhost:5000/product/3 -X DELETE
```

4. **Получение информации о товаре по его идентификатору**

```bash
curl http://localhost:5000/product/0
```

5. **Получение каталога товаров**

```bash
curl "http://localhost:5000/products?page=1&limit_per_page=2"
curl "http://localhost:5000/products?type=item"
```

## Часто используемые команды для работа с Docker-контейнерами

```bash
docker-compose up -d
docker-compose up -d --no-deps --build flask
docker kill -f $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
docker exec -it flask bash
```

## Комадны heroku

```bash
heroku login
git push origin heroku #Коммит в ветку heroku githubа автоматически инициирует деплой на heroku
heroku ps:scale web=1
heroku ps
heroku logs
```
