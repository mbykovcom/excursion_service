# realty-service

### Эндпоинты API сервиса

#### 1. /registration [POST] - Регистрация пользователя
Регистрация пользователя в системе, после регистрации отправляет письмо для подтверждения регистрации,
на указанный при регистрации email. 


##### Параметры запроса:
В *body* запроса передается объект модели **UserIn**.

##### Ответ сервера:
Сервер возвращает объект модели **UserOut**


#### 2. /login [POST] - Авторизация пользователя 
При успешной авторизации возрващает jwt-token.


##### Параметры запроса:
В *body* запроса передается объект модели **Auth**.

##### Ответ сервера:
Сервер возвращает объект модели **Token**


#### 3. /object [POST] - Создать объект 
Создать новый объект с аудио.


##### Параметры запроса:
В *body* запроса передается объект модели **ObjectIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **ObjectOut**


#### 4. /object [GET] - Получить список объектов 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает список объектов модели **ObjectOut**


#### 5. /object/{object_id} [GET] - Получить объект по id 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **ObjectOut**


#### 6. /object/{object_id} [PUT] - Обновить информацию объекта 
Обновить поля объекта

##### Параметры запроса:
В *body* запроса передается объект модели **ObjectIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает обновленный объект модели **ObjectOut**


#### 7. /object/{object_id} [DELETE] - Удалить объект 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает удаленный объект модели **ObjectOut**


#### 8. /route [POST] - Создать маршрут 
Создать новый маршрут.


##### Параметры запроса:
В *body* запроса передается объект модели **RouteIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **RouteOut**


#### 9. /route [GET] - Получить список маршрутов 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает список объектов модели **RouteOut**


#### 10. /route/{route_id} [GET] - Получить маршрут по id 
Получить детальную информацию маршрута

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **RouteDetails**


#### 11. /route/{route_id} [PUT] - Обновить данные маршрута по id 
Обновить поля маршрута

##### Параметры запроса:
В *body* запроса передается объект модели **RouteIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает обновленный объект модели **RouteOut**	


#### 12. /route/{route_id} [DELETE] - Удалить маршрут 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **RouteOut**


#### 13. /excursion [POST] - Создать экскурсию 
Создать новую экскурсию.


##### Параметры запроса:
В *body* запроса передается объект модели **ExcursionIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **ExcursionOut**


#### 14. /excursion [GET] - Получить список экскурсий 


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает список объектов модели **ExcursionOut**


#### 15. /excursion/{excursion_id} [POST] - Приобрести экскурсию 
Добавить экскурсию пользователю для доступа к прослушиванию.


##### Параметры запроса:
В *body* запроса передается объект модели **BuyIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **BuyOut**

#### 16. /excursion/{excursion_id} [GET] - Получить экскурсии по id 
Получить детальную информацию экскурсии

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **ExcursionDetails**


#### 17. /excursion/{excursion_id} [PUT] - Обновить данные экскурсии по id 
Обновить поля экскурсии

##### Параметры запроса:
В *body* запроса передается объект модели **ExcursionIn**.\
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает обновленный объект модели **ExcursionOut**	


#### 18. /excursion/{excursion_id} [DELETE] - Удалить экскурсию


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **ExcursionOut**


#### 19. /user/excursion [GET] - Получить список приобретенных экскурсий


##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает список объектов модели **UserExcursion**


#### 20. /user/excursion/{user_excursion_id} [GET] - Получить детальную информацию экскурсии у пользователя
Получить детальную информацию экскурсии у пользователя

	
##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации 

##### Ответ сервера:
Сервер возвращает объект модели **UserExcursionDetails**


#### 21. /statistics/user [GET] - Получить статистику кол-ва новых пользователей
Получить статистику кол-ва новых пользователей за указанное время

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации.\
В *path* запроса передаются параметры:
- **start** - начало отсчета для статистики (необязательное поле)
- **end** - конец отсчета для статистики (необязательное поле)

##### Ответ сервера:
Сервер возвращает объект модели **Statistics**


#### 22. /statistics/excursion [GET] - Получить статистику кол-ва покупок
Получить статистику кол-ва покупок экскурсий за указанное время

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации.\
В *path* запроса передаются параметры:
- **start** - начало отсчета для статистики (необязательное поле)
- **end** - конец отсчета для статистики (необязательное поле)

##### Ответ сервера:
Сервер возвращает объект модели **Statistics**


#### 23. /statistics/listening [GET] - Получить статистику кол-ва прослушиваний
Получить статистику кол-ва прослушиваний за указанное время

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации.\
В *path* запроса передаются параметры:
- **start** - начало отсчета для статистики (необязательное поле)
- **end** - конец отсчета для статистики (необязательное поле)

##### Ответ сервера:
Сервер возвращает объект модели **Statistics**


#### 24. /statistics/excursion [GET] - Получить статистику кол-ва продаж
Получить статистику кол-ва продаж за указанное время

##### Параметры запроса:
В *header* запроса передается параметр **jwt** с данными токена полученного при авторизации.\
В *path* запроса передаются параметры:
- **start** - начало отсчета для статистики (необязательное поле)
- **end** - конец отсчета для статистики (необязательное поле)

##### Ответ сервера:
Сервер возвращает объект модели **Statistics**


### Модели входящих и исходящих данных API


##### UserIn:

    {
        email*: string($email)
        title: Email
        The email a user
        
        password*: string
        title: Password
        minLength: 4
        The password a user
        
        name*: string
        title: Name
        User name in the service

    }

##### UserOut:

    {
        id: int
        title: User Id
        The id a user
        
        email: string($email)
        title: Email
        The email a user
        
        name: string
        title: Name
        User name in the service
        
        role: string
        title: Role
        The role a user in app
        
        date_registration: string
        title: Date Registration
        Date of user registration in the system
    }


##### Auth:

    {
        email*: string($email)
        title: Email
        The email a user
        
        password*: string
        title: Password
        minLength: 4
        The password a user
    }

##### Token:
    {
        access_token: string
        title: Access Token
        
        token_type: string
        title: Token Type
    }


##### ObjectIn:
    {
        name*: string
        title: Name
        The name of the object
        
        location*: tuple(lat, lon)
        title: Location
        The coordinates of the location
        
        url_audio*: string
        title: Audio
        Url audio
    }
    
##### ObjectOut:
    {
        id: int
        title: Object Id
        
        name: string
        title: Name
        The name of the object
        
        location: tuple(lat, lon)
        title: Location
        The coordinates of the location
        
        url_audio: string
        title: Audio
        Url audio
    }


##### RouteIn:
    {
        name*: string
        title: Name
        The name of the route
        
        route*: List[int]
        title: Route Point
        Sequential list of objects
    }
    
##### RouteOut:
    {
        id: int
        title: Route Id
        
        name: string
        title: Name
        The name of the route
        
        route: List[int]
        title: Route Point
        Sequential list of objects
    }


##### RouteDetails:
    {
        id: int
        title: Route Id
        
        name: string
        title: Name
        The name of the route
        
        route: List[ObjectsOut]
        title: Route Point
        Sequential list of objects
    }


##### ExcursionIn:
    {
        name*: string
        title: Name
        The name of the route
        
        description*: string
        title: Description
        The description of a excursion
        
        id_route*: int
        title: Route Id
    }
    
##### ExcursionOut:
    {
        id: int
        title: Route Id
        
        id_route: int
        title: Route Id
        
        name: string
        title: Name
        The name of the route
        
        description: string
        title: Description
        The description of a excursion
    }


##### ExcursionDetails
    {
        id: int
        title: Route Id
        
        name: string
        title: Name
        The name of the route
        
        description: string
        title: Description
        The description of a excursion
        
        route: RouteDetails
        title: Route
    }


##### UserExcursion
    {
        id: int
        title: User Excursion Id
        
        excursion: str
        title: Name Excursion
        
        last_point: str
        title: Last Point
        The point where we stopped
        
        date_added: datetime
        title: Data Added
    }
    
##### UserExcursionDetails
    {
        id: int
        title: User Excursion Id
        
        excursion: ExcursionDetails
        title: Data Excursion
        
        last_point: str
        title: Last Point
        The point where we stopped
        
        date_added: datetime
        title: Data Added
    }

##### BuyIn:
    {
        id_excursion*: int
        title: Excursion Id
        
        id_user*: int
        title: User Id
    }
    
##### BuyOut:
    {
        id: int
        title: Route Id
        
        id_excursion: int
        title: Excursion Id
        
        id_user: int
        title: User Id
        
        date_buy: datetime
        title: Date of buying
    }

##### Statistics:
    {
        type: str
        title: Type Statistics
        
        data: dict
        title: Data Statistics
    }




### Модели данных MongoDB

##### Objects
- _id: int
- name: str
- location: tuple('lat', 'lon')
- url_audio: str

##### Routes
- _id: int
- name: str
- route: List[Objects]

##### Excursion
- _id: int
- id_route: int
- name: str
- description: str
- price: float

##### Users
- _id: int
- name: str
- role: str
- email: str
- hash_password: str
- is_active: bool
- date_registration: datetime

##### SelectedExcursions
- _id: int
- id_user: int
- id_excursion: int
- last_point: int
- date_added: datetime

##### Bue
- _id: int
- id_user: int
- id_excursion: int
- date_buy: datetime

##### Listening
- _id: int
- id_user: int
- id_excursion: int
- id_object: int
- date_listening: datetime

##### TableKeys
- _id: ObjectId
- table: str
- last_id: int