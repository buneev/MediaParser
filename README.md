## Микросервис для парсинга новостных веб-ресурсов

### Описание
Микросервис реализован на aiohttp и scrapy. Предназначен для парсинга новостных веб-ресурсов

### Запуск в docker
1) docker build -t web_scraping_i .
2) docker run --name web_scraping -p 5858:5858 -d --restart=always  web_scraping_i
or
2) docker run --name web_scraping -p 5858:5858 -it --rm -v /home/ivan/git/MediaParser/MediaParser/src/data:/code/src/data  web_scraping_i

### Запуск локально
* Запуск парсинга:
scrapy crawl ria -o ../data/output.json

* Запуск парсинга в debug (vscode):
f5 run_debug.py 


### API

| Endpoint        | HTTP Method | Result                  |
|-----------------|-------------|-------------------------|
| /run_parse      | POST        | Run web scraping        |

Пример post запроса: {"spider_name": "ria", "make_import": false}

Тело post запроса:
* spider_name - имя паука (новостного сайта)
* make_import - делать ли импорт по адресу: http://127.0.0.1:8000/article/api/ (репозиторий blog)


### Реализованно
* Запуск парсинга статей через endpoint
* Парсинг статей с главной страницы "РИА новости" и отправка спарсенных данных на
  DRF api (репозиторий blog)

### Планируется
* Дописать handle для парсинга проксей, а после закинуть их в redis

