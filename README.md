Tatsiana Valenteychik
Домашнее задание
Системы контроля версии Git.Flask.
Разработка API на Flask.

1. Необходимо разработать REST API, предоставляющее возможность ведения блога.
2. API должен иметь минимум 3 сущности:
a.	Пользователь
b.	Пост
с.  Комментарий
3. Пользователь должен иметь возможность:
a.	создать, прочитатьб изменить, удалить пост
b. получить список всех постов
c. добавить и удалить комментарий

4. Задание должно быть выполнено с помощью фреймворка Flask.
5. Задание необходимо предоставить в виде архива с исходными кодом или ссылки на репозиторий в github/gitlab
a.	помимо кода, должна быть краткая инструкция по запуску задания
b.	в инструкции необходимо указать примеры тела запросов, HTTP метод и соответствующие URL для осуществления операций

Решение.

Проект попускается через https://web.postman.com.
Используется URL: 
localhost:5000/post
localhost:5000/post/reaction
localhost:5000/post/post_id
localhost:5000/post/post_id/reactions

Данные для тестирования.
{"body": "Hello World", "author": "@aqaguy"}
{"body": "Hello", "author": "@aqaguy"}
{"body": "Sun", "author": "@aqaguy"}
{"body": "Sun, Sun", "author": "@aqaguy"} - добавление и удаление поста.
 
Инструкция:
1. Создали папку Rest_API_home, в ней создали файлы наших сущностей:
  -Пользователи (user.py)
class User:
    def __init__(self, username: str):
        self.username = username


  -Пост (post.py)
  class Post:
    def __init__(self, post_id, body, author):
        self.post_id = post_id
        self.body = body
        self.author = author
        self.reactions = []

  -Комментарий (reaction.py)
  class Reaction:
    def __init__(self, reaction_id, post_id, user_id, reaction_type):
        self.reaction_id = reaction_id
        self.post_id = post_id
        self.user_id = user_id
        self.reaction_type = reaction_type

2. Создали папку main.py и написали код

Исходный код:
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

class Post:
    def __init__(self, post_id, body, author):
        self.post_id = post_id
        self.body = body
        self.author = author
        self.reactions = []

class Reaction:
    def __init__(self, reaction_id, post_id, user_id, reaction_type):
        self.reaction_id = reaction_id
        self.post_id = post_id
        self.user_id = user_id
        self.reaction_type = reaction_type

posts = [] 
reactions = []

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})

# Создание поста
@app.route('/post', methods=['POST'])
def create_post():
    post_json = request.json
    body = post_json.get('body')
    author = post_json.get('author')
    post_id = str(uuid4())
    post = Post(post_id, body, author)
    posts.append(post)
    return jsonify({'status': 'success', 'post_id': post_id}), 201

# Обновление поста
@app.route('/post/<post_id>', methods=['PUT'])
def update_post(post_id):
    post_json = request.json
    updated_body = post_json.get('body')
    updated_author = post_json.get('author')

    for post in posts:
        if post.post_id == post_id:
            if updated_body:
                post.body = updated_body
            if updated_author:
                post.author = updated_author
            return jsonify({'message': 'Post updated successfully'}), 200
    return jsonify({'message': 'Post not found'}), 404

# Получение информации о посте
@app.route('/post/<post_id>', methods=['GET'])
def read_post(post_id):
    post = next((post for post in posts if post.post_id == post_id), None)
    if post:
        post_data = {'post_id': post.post_id, 'body': post.body, 'author': post.author, 'reactions': [reaction.reaction_type for reaction in post.reactions]}
        return jsonify({'post': post_data})
    else:
        return jsonify({'message': 'Post not found'}), 404

# Создание реакции на пост
@app.route('/post/reaction', methods=['POST'])
def create_reaction():
    reaction_json = request.json
    post_id = reaction_json.get('post_id')
    user_id = reaction_json.get('user_id')
    reaction_type = reaction_json.get('reaction_type')
    reaction_id = str(uuid4())
    reaction = Reaction(reaction_id, post_id, user_id, reaction_type)
    reactions.append(reaction)
    post = next((post for post in posts if post.post_id == post_id), None)
    if post:
        post.reactions.append(reaction)
    return jsonify({'status': 'success', 'reaction_id': reaction_id}), 201

# Получение всех реакций на пост
@app.route('/post/<post_id>/reactions', methods=['GET'])
def get_reactions(post_id):
    post_reactions = [reaction for reaction in reactions if reaction.post_id == post_id]
    reactions_list = [{'reaction_id': reaction.reaction_id, 'user_id': reaction.user_id, 'reaction_type': reaction.reaction_type} for reaction in post_reactions]
    return jsonify({'reactions': reactions_list})

# Получение списка всех постов
@app.route('/post', methods=['GET'])
def read_posts():
    posts_list = [{'post_id': post.post_id, 'body': post.body, 'author': post.author} for post in posts]
    return jsonify({'posts': posts_list})

# Удаление поста
@app.route('/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    for i, post in enumerate(posts):
        if post.post_id == post_id:
            del posts[i]
            return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

    3. Через https://web.postman.com проверили работу нашего кода.

