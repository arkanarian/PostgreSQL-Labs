# Описание сущностей
(имя поля, тип, ограничения, связь с другими сущностями)

## Клиент (Client)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| first_name | VARCHAR(50) | not null | имя |
| last_name | VARCHAR(50) | not null | фамилия |
| birth_date | DATE | blank=True | дата рождения |
| telephone | VARCHAR(10) | blank=True, unique | номер телефона |
| passport_id | VARCHAR(10) | not null, unique | id пасспорта |
| family | ForeignKey(Family) | not null | сеья к которой клиент относиться |
## Семья (Family)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| room | ForeignKey(Room) | not null | комната клиента (у нескольких клиентов может быть одна комната) |
| guide | ForeignKey(Guide) | not null | гид клиента |
| tours | ManyToMany(Tour) | not null | экскурсии которые купила семья (покупается на всю семью, а не на одного клиента) |
## Комната (Room)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| card | fk | not null | внешний ключ на карту клиента |
| floor | INTEGER | not null | этаж комнаты |
| beds | INTEGER | not null | количесво кроватей |
| number | INTEGER | not null | номер комнаты |
| price | DECIMAL | not null | цена комнаты |
| isMiniBar | BOOLEAN | not null | есть ли минибар |
| date_enter | DATE | not null | дата занятия комнаты |
| date_leave | DATE | not null | дата освобождения комнаты |
## Карточка (Card)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| number | VARCHAR(16) | not null | ФИО пользователя |
| room | OneToOneField(Room) | not null | комната карточки |
## Гид (Guide)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| first_name | VARCHAR(50) | not null | имя гида |
| last_name | VARCHAR(50) | not null | фамилия гида |
| experience | INTEGER | not null | профессиональный опыт гида (в годах) |
| isFree | BOOLEAN | not null | свободен ли гид для новый семей |
## Экскурсия (Tour)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| title | VARCHAR(50) | not null | название экскурсии |
| places | VARCHAR(255) | not null | места которые будут посещены |
| price | INTEGER | not null | стоимость экскурсии для одной семьи |
| clients_amount | INTEGER | - | количество клиентов которые купили экскурсию |
| is_closed | BOOLEAN | - | открыта ли экскурсия, или она уже прошла |
| date_start | DATE | not null | дата начала экскурсии (день:час) |
| date_end | DATE | not null | дата конца экскурсии (день:час) |
## Абонемент Сауна (Sauna)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| name | VARCHAR(128) | not null | ФИО пользователя |
| post | VARCHAR(50) | not null | занимаемая должность |
| department | fk | not null | отделение клиники |
| experience | int | not null | опыт работы |
## Отделения (Departments)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| name | VARCHAR(128) | not null | название отделения |
address | VARCHAR(128) | not null | адрес отделения |
## Роли (Roles)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| name | VARCHAR(50) | not null | название роли |
| permission | VARCHAR(128) | not null | право пользователя |
## Логи (Logs)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| user | fk | not null | внешний ключ на пользователя |
| type | VARCHAR(50) | not null | тип лога(CREATE/UPDATE/DELETE) |
| representation | VARCHAR(255) | not null | строковое представление изменённого кортежа |