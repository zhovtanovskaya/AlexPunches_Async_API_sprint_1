# Схема Mongo

## Как подключиться к Atlas

Учебная версия Mongo создана в Atlas. Пароль: vAhgeeoxP8crYvpE
```shell
mongosh "mongodb+srv://cluster0.ynuujij.mongodb.net/myFirstDatabase" --apiVersion 1 --username yana
```

База данных с коллекцией `reactions` называется `ugc`:
```
mongosh> use ugc
mongosh> db.reactions.find()
```
