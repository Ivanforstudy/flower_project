{% extends 'main/base.html' %}
{% block title %}Вход{% endblock %}
{% block content %}
<h2>Вход</h2>
<form method="post">
    {% csrf_token %}
    <p>Имя пользователя: <input type="text" name="username"></p>
    <p>Пароль: <input type="password" name="password"></p>
    <button type="submit">Войти</button>
</form>
{% endblock %}
