#!/usr/bin/env python3
import sys, os
import datetime
import pika
import logging
from constants import FILE_NAME, QUEUE, HOST, CONSUMER_LOGS

logging.basicConfig(level=logging.ERROR, filename=CONSUMER_LOGS, format='%(asctime)s %(levelname)s:%(message)s')

def pv_simulator(current_time):
        pv_value = 0
        current_time = current_time.hour + current_time.minute/60
        if 15 >= current_time >= 6:
            pv_value = current_time**2*0.0138
        elif 21 >= current_time > 15:
            pv_value = (-current_time**2 + 450)*0.0138
        return abs(pv_value) * 1000

def save_output(body):
    output_file = open(FILE_NAME, "a")
    current_time = datetime.datetime.now()
    pv_value = int(pv_simulator(current_time))
    meter_value = int(body.decode("utf-8"))
    total = pv_value + meter_value
    print (f'Meter value: {meter_value}, PV value: {pv_value}, Total: {total},'
        f' Time: {current_time.hour}:{current_time.minute}:{current_time.second}')
    output_file.write(f'Meter value is {meter_value} watt, PV simulation value is {pv_value} watt and total is'
        f' {total} watt with timestamp {current_time}\n')
    output_file.close()

def callback(ch, method, properties, body):
    save_output(body)

def main(channel):
    try:
        channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
        print(f' [-] Writing the messages in {FILE_NAME} file. To exit please press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed as e:
        logging.error(f'Connection closed unexpectedly for thread with exception {e}')


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
        channel = connection.channel()
        main(channel)
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        logging.error('Connection to RabbitMQ was not established. Please re-run the RabitMQ server')
        print('Connection to RabbitMQ was not established. Please re-run the RabitMQ server')
        try:
            logging.error('System exits because of rabitmq connection error')
            sys.exit(0)
        except SystemExit:
            os._exit(0)