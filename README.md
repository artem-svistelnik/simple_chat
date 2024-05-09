# simple_chat

*To start the project you need to execute:**

* clone project repo
* Create an .env file and populate it following the default.env file example
* execute the command `make build`
* execute the command `make run`
* execute the command `make cmd`

Apply migration

in container console 
* execute the command `python manage.py migrate`

* execute the command `make restart`



* for load dump use `python manage.py loaddata db_dump.json`

**Description of requests :**

[isi_chat.postman_collection.json](isi_chat.postman_collection.json) -  collection for you postman

Get Token
http://0.0.0.0:8000/api/auth/token/

* 1)create thread POST http://0.0.0.0:8000/api/chat/threads/
* 2)removing a thread DELETE http://0.0.0.0:8000/api/chat/threads/:pk/
* 3)retrieving the list of threads for any user
  * 3.1)  1 var(my thread list) GET http://0.0.0.0:8000/api/chat/threads/
  * 3.2)  2 var(thread list by user id) GET http://0.0.0.0:8000/api/chat/threads/user/:pk/
* 4)creation of a message and retrieving message list for the thread
  * 4.1)creation of a message POST http://0.0.0.0:8000/api/chat/messages/:pk/
  * 4.2)retrieving message list for the thread GET http://0.0.0.0:8000/api/chat/messages/threads/:pk/
* 5)marking the message as read PUT http://0.0.0.0:8000/api/chat/messages/:pk/
* 6)retrieving a number of unread messages for the user GET api/chat/messages/unread/

Creds:
usernames: admin, user2, user3, user4, user5
password: admin