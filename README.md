# Inspector Habit — 🏆 [The Winner](https://tamtam.chat/botapichannel/AW5LroptDXs) of TamTam [bot developers contest](https://blog.tamtam.chat/ru/2019/08/02/)

Inspector Habit is a [TamTam](https://tamtam.chat/) bot which helps people to develop good habits and break bad ones. Users can also plan their day and create reminders via voice messages.


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

## Use case

There are three main functions in the menu: **🗓 Habits**, **📝 Plans** and **🔔 Reminders**.

![1](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/1.png)

### 🗓 Habits

![2](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/2.png)

Let's see current active habits.

![3](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/3.png)

And let's create a new one.

![4](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/4.png)

![5](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/5.png)

When check time is coming, we will get the following message from Inspector Habit.

![6](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/6.png)

Suppose we kept our promise and tap **✅ Yes**.

![7](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/7.png)

### 📝 Plans

![8](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/8.png)

Let's create today plan.

![9](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/9.png)

Ok, plan is ready.

![10](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/10.png)

Now we can report.

![11](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/11.png)

Suppose that we have done README.

![12](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/12.png)

When report is ended we will see the following.

![13](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/13.png)

And can create tomorrow plan.

### **🔔 Reminders**

![14](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/14.png)

How to create reminders?

![15](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/15.png)

Ok, we don't have any reminders, so let's create the first one.

![16](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/16.png)

And we get a reminder in time.

![17](https://raw.githubusercontent.com/Macket/inspector_habit_tamtam/master/img/readme/17.png)