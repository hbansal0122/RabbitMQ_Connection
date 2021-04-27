# RabbitMQ Connection establishment

## Description
This is a assignment for The mobility house. This application is combination of a producer which produces a random meter value and passes that value to broker which in out case is RabbitMQ. RabbitMQ passes this value to consumer which consumes this value and also simulate PV value. After consuming and generating pv value, consumer also output the data in results.txt file.

## RabbitMQ Installiation steps
``` 
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install erlang
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
``` 

### RabbitMQ user management steps (Optional: Not used in our assignment as this is single user system)
``` 
sudo rabbitmq-plugins enable rabbitmq_management
```
user is the username and password is the new password
```
sudo rabbitmqctl add_user user password
```
giving that user adiministraitve rights
```
sudo rabbitmqctl set_user_tags user administrator
sudo rabbitmqctl set_permissions -p / user "." "." "."
```

## Python installation and creating virtual environment 
Step 1: Install Python 3 from https://www.python.org/downloads/

Step 2: Create virtual environment for keeping dependencies aligned 

``` 
python3 -m venv env_name
```

Step 3: Activate virtual envrionment by 

``` 
source env_name/bin/activate 
```

Step 4: Install dependencies by 
``` 
pip3 install -r requirements.txt
```

## Testing
To run the tests, please run below command. Your current directory should be root to run the command or please change the command appropriately.
```
python3 -m unittest tests/*_test.py
```


## Running steps
To run the scripts, it is required that you start the RabbitMQ server before hand. To do so on Ubunutu please run below commands 
``` 
sudo systemctl start rabbitmq-server
``` 

To stop the RabbitMQ server, you can use
```
sudo systemctl stop rabbitmq-server
``` 

To start the scripts, you start the first script.
producer.py will start generating random meter values and pass them to broker
```
python3 producer.py
``` 
and next one is 
consumer.py will start consuming the meter values and generate simulated pv values and output them to file
```
python3 consumer.py
``` 
