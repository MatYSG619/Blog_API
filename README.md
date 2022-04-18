# Blog_API

## Описание
Реализация Rest API для системы комментариев блога

##### Функциональные требования:
- Добавление статьи.
- Добавление комментария к статье.
- Добавление коментария в ответ на другой комментарий. Вложенность - любая
- Получение всех комментариев к статье вплоть до 3 уровня вложенности.
- Получение всех вложенных комментариев для комментария 3 уровня.
- По ответу API комментариев можно воссоздать древовидную структуру.

##### Нефункциональные требования:
- Использование Django ORM.
- Следование принципам REST.
- Число запросов к базе данных не должно напрямую зависеть от количества комментариев, уровня вложенности.
- Решение в виде репозитория на Github, Gitlab или Bitbucket.
- readme, в котором указано, как собирать и запускать проект. Зависимости указать в requirements.txt либо использовать poetry/pipenv.
- Использование свежих версий python и Django.

## Версия Python
Python 3.10

## Установка
```console
git clone https://github.com/MatYSG619/Blog_API/tree/master
cd Blog_API
pip install -r requirenments.txt
python manage.py runserver
```
## models
#### Article
|field|type|
|-----|----|
|title|CharField(max_length=150)|
|description|TextField()|
|created|DateTimeField(auto_now_add=True)|

#### Comment
|field|type|
|-----|----|
|article|ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')|
|text|TextField()|
|level|PositiveIntegerField(default=0)|
|parent|ForeignKey('self',verbose_name='Родитель',on_delete=models.SET_NULL,blank=True,null=True,related_name='children')|

## API

### Просмотр всех статей

##### request
|type|url|
|----|---|
|GET|/api/articles/|

##### return example
```json
{
    "articles": [
        {
            "title": "Первая статья",
            "description": "Описание первой статьи",
            "created": "2022-04-16 07:05:41.374739+00:00"
        },
        {
            "title": "Вторая статья",
            "description": "Описание второй статьи",
            "created": "2022-04-16 07:33:43.139923+00:00"
        }
    ]
}
```

### Добавление статьи

##### request
|type|url|json params|
|----|---|-----------|
|POST|/api/articles/|```{"article": {"title": "str64 param","description": "text param", "created": "text param"}}```|

##### return
```json
{"success": "Article '{article.title}' created successfully"}
```

##### about
Добавление статьи происходит номинально, в качестве сущности к которой будут крепиться комментарии

### Добавление комментария к статье

##### request
|type|url|json params|
|----|---|-----------|
|POST|/api/articles/<int:pk>/|{"comment": {"text": "text param"}}|

##### return
```json
{"success": "Comment '{сomment.id}' create"}
```

##### about
В url необходимо вставить id статьи, чтобы оставить комментарий.<br/>
В json params указывается только текст комментария, все остальное сделает программа, а именно укажет уровень и привяжет комментарий к статье.<br/>
Нумерация уровня начинается с 0.

### Ответ на комментарий

##### request
|type|url|json params|
|----|---|-----------|
|POST|api/comments/<int:comment_id>/|{"comment": {"text": "text param"}}|

##### return
```json
{"success": "Reply '{comment.id}' on the comment '{comment.id}' create"}
```

##### about
В url необходимо вставить id комментария, на который оставляется ответ
В json params указывается только текст ответа.

### Получение всех комментариев к статье

##### request
|type|url|
|----|---|
|GET|api/comments/article/<int:pk>/|

##### return example
```json
{
    "article": [
        {
            "title": "Вторая статья",
            "description": "Описание второй статьи",
            "created": "2022-04-16T07:33:43.139923Z",
            "comments": [
                {
                    "article": 2,
                    "text": "Комментарий ко второй статье",
                    "level": 0,
                    "children": [
                        {
                            "article": 2,
                            "text": "Ответ на комментарий из второй статьи",
                            "level": 1,
                            "children": []
                        }
                    ]
                },
                {
                    "article": 2,
                    "text": "Второй комментарий ко второй статье",
                    "level": 0,
                    "children": [
                        {
                            "article": 2,
                            "text": "Ответ на комментарий",
                            "level": 1,
                            "children": [
                                {
                                    "article": 2,
                                    "text": "Еще один ответ на комментарий",
                                    "level": 2,
                                    "children": [
                                        {}
                                    ]
                                },
                                {
                                    "article": 2,
                                    "text": "Ответ на очередной комментарий",
                                    "level": 2,
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "article": 2,
                    "text": "Третий комментарий ко второй статье",
                    "level": 0,
                    "children": []
                }
            ]
        }
    ]
}
```

##### about
В url указывается id статьи, на который требуется увидеть комментарии и ответы. <br/>
Комментарии и ответы выведены вплоть до 3 уровня. <br/>
API комментариев имеет древовидную структуру. <br/>
