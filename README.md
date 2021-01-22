# Inspector Habit — 🏆 [Winner](https://tamtam.chat/botapichannel/AW5LroptDXs) of TamTam [bot developers contest](https://blog.tamtam.chat/ru/2019/08/02/)

Inspector Habit is a [TamTam](https://tamtam.chat/) bot which helps people to develop good habits and break bad ones. Users also can plan their day and create reminders via voice messages.


## Getting Started

Inspector Habit bot requires Python 3.7 and packages specified in ```requirements.txt```.

You can install them with

```
pip install -r requirements.txt
```

Before you start Inspector Habit it is necessary to create ```.env``` file:

```
touch .env
```

and fill in this file according to the example below:

```
DEBUG = True

TT_BOT_API_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ADMIN_ID = XXXXXXXXXXX

DATABASE_URL = postgres://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

DB_NAME = inspector_habit_db
DB_USER = user
DB_PASSWORD = XXXXXXXXXXX
DB_HOST = localhost
```

```DEBUG``` should be **False** in prod

```TT_BOT_API_TOKEN``` is the token got from [PrimeBot](https://tt.me/primebot)

```ADMIN_ID``` is the TamTam id of the admin

```DATABASE_URL``` is used to access the database in prod

```DB_NAME```, ```DB_USER```, ```DB_PASSWORD``` and  ```DB_HOST```  are used to access the database in dev

Then you can start Inspector Habit with this command:

```
python main.py
```

