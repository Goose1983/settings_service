# Шаблон сервиса для проекта MATRIX

## app.py
Входная точка приложения, "грязный" модуль, в котором инстанцируем все зависимости


## api/controllers
Пакет с контроллерами endpoint-ов

## api/schemas
Пакет с описанием схем запросов

## api/injections.py
Модуль с описанием рантайм зависимостей контроллеров

## api/router.py
Модуль, собирающий маршруты всех контроллеров

## core/config.py
Модуль конфигурации, которая тянется из переменных окружения или env-файла

## core/data_source.py
Модуль с описанием подключения к БД

## models
Пакет с описаниями моделей в БД

# Запуск в окружении

## Запуск контейнера с ораклом (нашел только 12-й, но текущий клиент работает ок)
```
docker run -d -it --name oracle -P store/oracle/database-enterprise:12.2.0.1
docker port oracle
```
Вывод будет похож на
```
5500/tcp -> 0.0.0.0:55000
1521/tcp -> 0.0.0.0:55001
```

Берём порт, в который замапился 1521/tcp и подставляем его в src/core/config.py/DATABASE_PORT

## Настройка БД
Дефолтный логин/пароль - 

Создает схему/пользователя MATRIX

DDL для тестовой таблицы
```
CREATE TABLE "MATRIX"."TEMPLATE" 
   (	"ID" VARCHAR2(32), 
	"NAME" VARCHAR2(100), 
	"VALUE" VARCHAR2(100), 
	"VERSION" NUMBER(*,0), 
	 CONSTRAINT "NEWTABLE_PK" PRIMARY KEY ("ID")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS"  ENABLE
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;

CREATE UNIQUE INDEX "MATRIX"."NEWTABLE_PK" ON "MATRIX"."TEMPLATE" ("ID") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;
```

## Запуск сервиса
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn src.app:app --host 0.0.0.0 --port 8000
```

## Тестовый запрос
```
curl -X POST -d @test_data/request.json localhost:8000/api/v1/template/insert_example
```

## Сборка и пуш образа
Предварительно завести для проекта репозиторий в корпоративном artifactory (https://wiki.cinimex.ru/pages/viewpage.action?pageId=37591118)
Можно для начала завести учетку на dockerhub и экспериментировать с ней (https://hub.docker.com). Там же создать репозиторий, допустим, вы назвали его template.
```
docker build -t artifactory.cinimex.ru/alfmatrix_docker/settings:0.1 .
docker push artifactory.cinimex.ru/alfmatrix_docker/settings:0.1
```
### Запуск образа локально
```
docker run -p 8000:8000 -e DATABASE_HOST=ХОСТ_БД \
                        -e DATABASE_PORT=ПОРТ_БД \
                        -e DATABASE_USER=ПОЛЬЗОВАТЕЛЬ_БД \
                        -e DATABASE_PASSWORD=ПАРОЛЬ_БД \
                        -e DATABASE_SERVICE_NAME=СЕРВИС_БД \
                        -e DATABASE_POOL_SIZE=РАЗМЕР_ПУЛА_КОННЕКТОВ \
                        {ваш_логин_на_докерхаб}/template:1
```

## Развернуть в k8s
В проде будем экспоузить через Ingress, но для разработки можно не заморачиваться
```
kubectl create namespace template 
kubectl apply -f k8s/deployment -n template
kubectl expose deployment template-deployment --type=NodePort --name=template-service -n template
kubectl describe service template-service -n template # Покажет порт, на который замапился сервис
```