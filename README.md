# *Chatscape*
---
---
**Chatscape** is a chat application where you can chat with other users and make friends.
___
This project is built using **django** and **websockets**. [django channels](https://github.com/django/channels) is used to handle websockets.

### How to setup?

Navigate to the directory where you want to store the project and open command line there.

Now from the command line,

##### STEP 0 (clone the repo)
```
git clone https://github.com/j-yeskay/chatscape-django.git
cd chatscape-django
```

##### STEP 1 (create a venv virtual environment)
``python -m venv virt``

Activate the virtual environment by

**For Windows on cmd**
``virt\Scripts\activate``

**For Mac**
``source virt/bin/activate``

##### STEP 2 (install the dependencies)
``pip install -r requirements.txt``

##### STEP 3 (create SECRET_KEY and set DEBUG = True in settings . py )

Now in the command prompt
Type **python** and hit enter.
```
>>>import secrets
>>>secrets.token_hex(24)
<a secret key will be generated>
```
Copy the generated secret key and in the **settings . py** file
Change the code

**FROM THIS**
``SECRET_KEY = config('SECRET_KEY')``

**TO THIS**
``SECRET_KEY = < paste the generated secret key here>``

**AND FROM THIS**
``DEBUG = config('DEBUG', cast=bool, default = True)``

**TO THIS**
``DEBUG = True``

##### STEP 4 (specify a channel layer)

I have used **redis** as a backing store for the channel layer for this project. **(i recommend using docker  for redis).**
Start a redis server on port 6379 using docker by
``docker run -p 6379:6379 -d redis:5``

You can also use the **in-memory channel layer** that comes packaged with django channels.
**NOTE :(if you use the in-memory channel)**
change the following code in **settings . py** file.

**FROM THIS**
```
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```
**TO THIS**
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

##### STEP 5 (run the migrations)
```
python manage.py makemigrations
python manage.py migrate
```

##### STEP 6 (run the app)
```
python manage.py runserver
```













