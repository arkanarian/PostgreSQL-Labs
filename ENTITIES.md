# Описание сущностей
( field name, type, constraints, description с другими сущностями)

## Пользователь (User)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| username | VARCHAR(30) | NOT NULL, UNIQUE | имя пользователя |
| password | VARCHAR(100) | NOT NULL | пароль |
| email | VARCHAR(50) | UNIQUE | эл почта |
| telephone | VARCHAR(13) | UNIQUE | номер телефона |
| unblock_date | DATE | - | дата разблокировки пользователя |
___
## Страница Пользователя (Page)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| description | VARCHAR(300) | - | подписчики страницы |
| owner_id | INT | NOT NULL, UNIQUE, REFERENCES User(id) | пользователь к которому прикреплена эта страница |
## Подписчики страницы (Page_followers)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| page_id | INT | NOT NULL, REFERENCES Page(id) | страница на которую подписан пользователь |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь который подписан на страницу |
## Запросы на подписку на страницу (Page_follow_requests)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| page_id | INT | NOT NULL, REFERENCES Page(id) | страница на которую подписан пользователь |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь который подписан на страницу |
___
## Записка на странице (Note)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| title | VARCHAR(50) | - | заголовок записки |
| text | VARCHAR(2000) | - | текст записки |
| image_url | VARCHAR(300) | - | ссылка s3 на изображение |
| page_id | INT | NOT NULL, REFERENCES Page(id) | страница на которой создана записка |
| reply_to_id | INT | REFERENCES Note(id) | записка который репостит этот записку |
| date_created | DATE | NOT NULL | дата создания записки |
| date_updated | DATE | NOT NULL | дата последнего редактирования записки |
## Лайки на записке (Note_likes)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| note_id | INT | NOT NULL, REFERENCES Note(id) | записка |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь который лайкнул |
## Тэги записки (Note_tags)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| note_id | INT | NOT NULL, REFERENCES Note(id) | записка |
| tag_id | INT | NOT NULL, REFERENCES Tag(id) | тэг |
## Тег (Tag)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| title | VARCHAR(30) | NOT NULL | название тега |
___
## Сообщество (Community)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| name | VARCHAR(30) | NOT NULL | название сообщества |
| description | VARCHAR(200) | - | описание сообщества |
| category_id | INT | REFERENCES Category(id) | название сообщества |
| date_created | DATE | NOT NULL | дата создания сообщества |
| unblock_date | DATE | - | дата разблокировки сообщества |
## Администраторы сообщества (Community_admins)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| community_id | INT | NOT NULL, REFERENCES Community(id) | сообщество |
| user_id | INT | NOT NULL, REFERENCES User(id) | администратор |
## Подписчики сообщества (Community_followers)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| community_id | INT | NOT NULL, REFERENCES Community(id) | сообщество |
| user_id | INT | NOT NULL, REFERENCES User(id) | подписчик |
## Категория (Category)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| title | VARCHAR(30) | NOT NULL | название категории |
___
## Пост сообщества (Post)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| title | VARCHAR(50) | - | заголовок поста |
| text | VARCHAR(2000) | - | текст поста |
| image_url | VARCHAR(300) | - | ссылка s3 на изображение |
| community_id | INT | NOT NULL, REFERENCES Community(id) | страница на которой создан пост |
| reply_to_id | INT | REFERENCES Post(id) | пост который репостит этот пост |
| date_created | DATE | NOT NULL | дата создания поста |
| date_updated | DATE | - | дата последнего редактирования поста |
## Лайки на посте (Post_likes)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| post_id | INT | NOT NULL, REFERENCES Post(id) | пост |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь который лайкнул |
## Тэги поста (Post_tags)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| post_id | INT | NOT NULL, REFERENCES Post(id) | пост |
| tag_id | INT | NOT NULL, REFERENCES Tag(id) | тэг |
## Пользователи сохранившие пост (Post_saved)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| post_id | INT | NOT NULL, REFERENCES Post(id) | пост |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользовтель сохранивший пост |
___
## Комментарий (Comment)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| content | VARCHAR(300) | - | текстовый контент поста |
| document_id | INT | REFERENCES Document(id) | ссылка s3 на документ |
| owner_id | INT | NOT NULL, REFERENCES User(id) | пользователь который написал коммент |
| post_id | INT | NOT NULL, REFERENCES User(id) | пост под которым написан комент |
| reply_to_id | INT | NOT NULL, REFERENCES Comment(id) | комент к которому прикреплен данный комент |
| date_created | DATE | NOT NULL | дата создания коммента |
| date_edited | DATE | - | дата последнего редактирования комента |
## Лайки коммента (Comment_likes)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| post_id | INT | NOT NULL, REFERENCES Post(id) | пост |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь поставивший лайк |
## Дизлайки коммента (Comment_dislikes)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| post_id | INT | NOT NULL, REFERENCES Post(id) | пост |
| user_id | INT | NOT NULL, REFERENCES User(id) | пользователь поставивший дизлайк |
## Документ (Document)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| document_url | VARCHAR(300) | - | ссылка s3 на документ |
___
## Роли (Roles)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| name | VARCHAR(30) | NOT NULL | название роли |
| permission | VARCHAR(50) | NOT NULL | право пользователя |
___
## Логи (Logs)
| field name | type | constraints | description |
|:---:|:---:|:---|:---|
| id | INT | PRIMARY KEY | первичный ключ |
| user_id | INT | NOT NULL, REFERENCES User(id) | внешний ключ на пользователя |
| type | VARCHAR(20) | NOT NULL | тип лога(CREATE/UPDATE/DELETE) |
| message | VARCHAR(300) | NOT NULL | сообщение характеризующее лог |