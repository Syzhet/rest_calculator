# rest_calculator

## REST API - онлайн-кальклятор.

Исходный функционал:
- Выполнение простых математических операций.
- Валидация передаваемых значений.
- Документация по API.
- Запуск в docker-контэнере.


## Стек технологий 

<div>
  <a href="https://www.python.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  </a>
  <a href ="https://www.docker.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://github.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/github/github-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
</div>

Версии ПО:

- python: 3.10.4;
- fastapi: 0.85.1;
- uvicorn: 0.18.3;
- Docker: 20.10.18;
- docker-compose: 1.26.0.


# Установка проекта локально
Склонировать репозиторий на локальную машину:
```sh
git clone https://github.com/Syzhet/rest_calculator.git
```
Cоздать и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```

Запусите приложение командой:
```sh
uvicorn app:app --reload
```

# Запуск проекта в Docker контейнере
Установите Docker и docker-compose
```sh
sudo apt install docker.io 
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Cоздайте файл .env в корневой директории проекта содержанием:
- REP_NAME= имя репозитория на Docker Hub (либо внесите изменения в файл docker-compose.yaml для сборки и запуска контейнера локально);
- TAG= версия ообраза docker;
- PORT= порт для отправки http запросов.

Параметры запуска описаны в файлах docker-compose.yml.

Запустите docker-compose:
```sh
sudo docker-compose up -d
```

После сборки появляется 3 контейнера:

| Контайнер | Описание |
| ------ | ------ |
| calc_api | контейнер с запущенным приложением |


## Авторы проекта

- [Ионов А.В.](https://github.com/Syzhet) - Python разработчик.