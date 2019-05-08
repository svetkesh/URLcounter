# URLcounter
**Flask+Celery+MongoDB+AJAX+CSS example**

This project deals with **Celery** Tasks linked with frontend manipulations and web pages retrieving and parsing.

As user enter some URL and click "Submit" button **AJAX** sends a command to the **Flask** route to start task 
with given address as parameter.

Page recieve unique address for task status update.

Queue filled with **JSON** from task with status and result.

With results (counted HTML tags on the page) recived by page **JavaScript** builds nice chart for tags.

![](https://github.com/svetkesh/URLcounter/blob/master/screenshots/Screenshot%20at%202019-05-08%2000-44-37.png)

Some portion of data stored remotely in **MongoDB** instance (shard):

![](https://github.com/svetkesh/URLcounter/blob/master/screenshots/Screenshot%20at%202019-05-08%2001-59-56.png)

Here I select permisive option to deal with errors.
While input field only accept url-like strings, backend deal wrong addresses more gently with humble yellow bar shown at the end.  

![](https://github.com/svetkesh/URLcounter/blob/master/screenshots/Screenshot%20at%202019-05-08%2002-03-43.png)

And of cource I'd like to express my gratitude to the Autors who inspired me and shares their knowlege with World:

https://blog.miguelgrinberg.com/post/using-celery-with-flask

http://flask.pocoo.org/docs/1.0/patterns/jquery/

https://www.datasciencelearner.com/python-ajax-json-request-form-flask/
