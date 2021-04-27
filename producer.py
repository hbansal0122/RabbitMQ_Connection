#!/usr/bin/env python3

import datetime
import logging
import os
import random
import sys
import time

import pika

from constants import HOST, QUEUE, RANDOM_VALUE_START, \
    RANDOM_VALUE_END, HOURS_TO_RUN_SCRIPT, SLEEP_TIME, PRODUCER_LOGS

logging.basicConfig(level=logging.ERROR, filename=PRODUCER_LOGS, format='%(asctime)s %(levelname)s:%(message)s')


def transmit_message(channel_name, meter_value):
    """Transmit meter value on channel"""
    try:
        channel_name.basic_publish(exchange='', routing_key=QUEUE, body=str(meter_value))
        print(f'Meter value: {meter_value} watts')
        time.sleep(SLEEP_TIME)
    except pika.exceptions.ConnectionClosed as e:
        logging.error(f'Connection closed unexpectedly for thread with exception {e}')


def main(channel_name):
    """Main function which will run on producer script call"""
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=HOURS_TO_RUN_SCRIPT)
    while start_time <= end_time:
        meter_value = random.randint(RANDOM_VALUE_START, RANDOM_VALUE_END)
        transmit_message(channel_name, meter_value)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE)
        main(channel)
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        logging.error('Connection to RabbitMQ was not established. Please re-run the RabitMQ server')
        print('Connection to RabbitMQ was not established. Please re-run the RabitMQ server')
        try:
            logging.error('System exits because of rabbitmq connection error')
            sys.exit(0)
        except SystemExit:
            os._exit(0)
