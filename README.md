# xsolla-backend-2021-test

Test for Xsolla School 2021. Backend: RESTful API for e-commerce game developer's system.

**Задача**: реализация системы управления товарами для площадки электронной коммерции (продажа таких товаров, как игры, мерч, виртуальная валюта и др.)

## Обязательная часть

Реализовать методы API для операций CRUD по управлению товарами. Товар определяется уникальным идентификатором и обязательно должен иметь [SKU](https://ru.wikipedia.org/wiki/SKU), имя, тип, стоимость. Для создания API используется библиотека [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/index.html).

1. **Создание товара**. Метод генерирует и возвращает уникальный идентификатор товара.
2. **Редактирование товара**. Метод изменяет все данные о товаре по его идентификатору или SKU.
3. **Удаление товара по его идентификатору или SKU**.
4. **Получение информации о товаре по его идентификатору или SKU**.
5. **Получение каталога товаров**. Метод возвращает список всех добавленных товаров. Товаров может быть много. Необходимо предусмотреть возможность снижения нагрузки на сервис. **Вариант реализации**: возвращайте список товаров по частям.
6. [Разработать документацию в README](https://medium.com/xsolla-tech/tips-to-help-developer-improve-their-test-tasks-69d5a3b948d3). Обязательно укажите последовательность действий для запуска и локального тестирования API.

## Дополнительная часть - доработка системы управления товарами

1. Информация о товарах хранится в локальной базе данных mongodb, для работы с которой используется отображение объектов в документы (ODM) [MongoEngine](http://mongoengine.org/).
2. Создан скрипт `prepare_mongo.py`, который наполняет СУБД тестовыми данными из набора `test_dataset.json`.
3. Созданы модульные тесты
4. Фильтрация товаров по их типу и/или стоимости в **Методе получения каталога товаров**.
5. Спецификация OpenAPI [3.0](https://swagger.io/specification/). Документация для разработанного REST API.
6. Создать Dockerfile для создания образа приложения системы. Желательно наличие файла Docker-compose.
7. Развернуть приложение на [heroku](https://www.heroku.com/).
8. Реализовать frontend при помощи bootstrap.

## Способ тестирования приложения

Для запуска приложения необходимо перейти рабочую директорию проекта и в командной строке выполнить команду

```bash
python3 api.py
```

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
curl http://localhost:5000/products
```

## Запуск модульных тестов

```bash
python3 -m unittest -v utest_api_resources.py
```

## Работа с Docker-контейнерами

```bash
docker-compose up -d
docker-compose up -d --no-deps --build flask
docker kill -f $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
docker exec -it flask bash
docker login
docker build -t konstgav/api-xsolla-test:0.1 .
docker push konstgav/api-xsolla-test:0.1
docker container run -it --rm -p 5000:5000 konstgav/api-xsolla-test:0.1
docker create -it --name api-test -p 5000:5000 mongo
docker start api-test
docker stop api-test
```

Образ доступет по ссылке dockerhub