CONTINIOUS DEPLOYMENT
---------------------

### Development Methodology

1. Start new feature by creating new branch
2. Finish your feature by covering it with unit/integration tests
3. Launch your tests if all of them passed go to phase (4)
4. Launch your app if app is launched go to phase 5
5. Create a pull request to long-lasting branch (develop or master, depending on case)
6. Mark your task as fixed in youtrack


###``Remember``

1. Push to master only if:
   * you successfully build the project at your feature branch
   * you successfully passed the unit tests
2. Check that build is successfully built in Travis-CI before going home


Launching Software
------------------

## Component-by-Component

1. Celery: `celery -A natr worker -l debug`


## Configure Centrifugo under OSX

1. In case of OSX execute this bash script:

`route -n add -net 172.16.0.0./12 192.168.99.100`

## Using Docker

1. Run the whole project with `docker-compose up -d`
2. Check that everything is started ok `docker-compose ps`

API
---

API is constantly updated and documented by `http://127.0.0.1:8000/docs` address


RoadMap
---------

Формы/Документы

   - Заключение
   - Оценка эффективности на начало и каждые 6 месяцев

Интеграция с СЭД
   -

Кабинет ГП

Chat и Уведомления

Risk Ranging
  - Перекрестный анализ небольшой
  - Вручную

Отчеты ИСЭМ

Пользователи (ГП, Эксперты)

Права доступа


1. Предоставить Заказчику на согласование полный Дизайн модуля Эксперта ЦАМП 25.11.2015, ответственный - Дизайнер
2. Предоставить Заказчику на согласование полный Дизайн модуля Грантополучателя 26.11.2015, ответственный - Дизайнер
3. Предоставить демо версию модуля Эксперта ЦАМП для тестирования заказчику 03.12.2015, ответственные - Разработчики
4. Предоставить демо версию модуля Грантополучателя для тестирования заказчику 10.12.2015, ответственные - Разработчики
5. Учесть замечания Заказчика и предоставить исправленный вариант Дизайна до 01.12.2015, ответственный - Дизайнер
6. Учесть замечания Заказчика и предоставить исправленный вариант модуля Эксперта ЦАМП и Грантополучателя до 15.12.2015, ответственные - Разработчики


Notes
-----

Скоуп данных:
  На стороне ГП и эксперта:
     - Проекты в которых состоит
       /chat/project_list
     - История по проекту в котором было последнее самое недавнее сообщение
       /chat/history?project=...

  Открытие чат коннекта
     - CHAT#user_id e.g. CHAT#1, CHAT#2
  Обновления статуса коннекта каждые 30 секунд


Механизм отправки сообщения
  - клиент отправляет API запрос /chat/message
  - сообщение сохраняется в базе
  - сообщение распыляется всем пользователям группы
  - если чат открыт, то каунтер сбрасывается автоматически API запросом
  - иначе показываем обновленный каунтер
  - При открытии чат окна открывается проект в котором было написано последнее сообщение
