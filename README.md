## Парсер собирающий статьи с разных сайтов

### Описание

### Запуск
docker-compose up -d

### API

| Endpoint        | HTTP Method | Result                  |
|-----------------|-------------|-------------------------|
| article/api     | GET         | Get all articles        |
| article/api     | POST        | Add articles            |
| article/api/:id | GET         | Get a single article    |
| article/api/:id | PUT         | Update a single article |
| article/api/:id | DELETE      | Delete a single article |

### Реализованно
* Парсинг статей с главной страницы ria-новости, и отправка спарсенных данных
на DRF api.

### Планируется
* спарсить прокси и закинуть их в redis
* отображать / рассылать раз в неделю статьи с 3-5 новостных сайтов,
по заданным ключевым словам (война, кризис и т.д.)


