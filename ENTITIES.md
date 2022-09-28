# Описание сущностей
(имя поля, тип, ограничения, связь с другими сущностями)

## Пользователь (User)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| username | VARCHAR(50) | not null; unique | имя пользователя |
| password | VARCHAR(255) | not null | пароль |
| email | VARCHAR(100) | blank=True | эл почта |
| telephone | VARCHAR(10) | blank=True, unique | номер телефона |
| is_blocked | BOOLEAN | not null | заблокирован ли пользователь |
## Страница Пользователя (Page)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| owner | OneToOneField(User) | not null | пользователь к которому прикреплена эта страница |
| followers | ForeignKey(Room) | not null | подписчики страницы |
| unblock_date | DATE | - | дата разблокировки страницы |
## Пост (Post)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| title | VARCHAR(100) | not null | заголовок поста |
| likes | ForeignKey(User) | - | пользователи которые лайкнули пост |
| image_url | VARCHAR(255) | - | ссылка s3 на изображение |
| tag | ForeignKey(Tag) | not null | тег поста (тематика) |
| page | ForeignKey(Page) | not null | страница пользователя который создал пост |
| community | ForeignKey(Community) | not null | сообщество которое создало пост |
| repost | ForeignKey(Post) | not null | пост который репостит этот пост |
| date_created | DATE | not null | дата создания поста |
## Сообщество (Community)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| name | VARCHAR(50) | not null | название сообщества |
| admins | ManyToMany(User) | not null | администраторы сообщества |
| followers | ForeignKey(User) | not null | подписчики сообщества |
| category | ForeignKey(Category) | not null | категория сообщества |
| date_created | DATE | not null | дата создания сообщества |
| is_blocked | BOOLEAN | not null | заблокировано ли сообщество |
| unblock_date | DATE | - | дата разблокировки сообщества |
## Комментарий (Comment)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| content | VARCHAR(255) | not null | текстовый контент поста |
| image_url | VARCHAR(255) | - | ссылка s3 на изображение |
| valuable | ForeignKey(User) | - | пользователи которые посчитали коммент ценным |
| nonvaluable | ForeignKey(User) | - | пользователи которые посчитали коммент неценным |
| user | ForeignKey(User) | not null | пользователь который написал комент |
| post | ForeignKey(Post) | not null | пост под которым написан комент |
| reply_to | ForeignKey(Comment) | - | комент к которому прикреплен данный комент |
| date_created | DATE | not null | дата создания коммента |
| date_edited | DATE | - | дата последнего редактирования комента |
## Тег (Tag)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| title | VARCHAR(100) | not null | название тега |
## Категория (Category)
|имя поля | тип | ограничения | описание |
|:---:|:---:|:---:|:---:|
| id | pk | auto increment; not null; unique | первичный ключ |
| title | VARCHAR(100) | not null | название категории |
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
| user | ForeignKey(User) | not null | внешний ключ на пользователя |
| type | VARCHAR(50) | not null | тип лога(CREATE/UPDATE/DELETE) |
| representation | VARCHAR(255) | not null | строковое представление изменённого кортежа |