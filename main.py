import serial
import time

import datetime

from multiprocessing import Process, Manager
from drawing_thread import drawing_thread, data_format, data_type


def type_converter(d: str, d_type):
    if d_type == float:
        return float(d)
    elif d_type == int:
        return int(d)
    elif type(d_type) == str:
        if d_type[0] == 's':
            return [int(i) for i in d.split(d_type[1:])]


def parse_data(data: str) -> dict:
    result = dict()

    if not (len(data.split(',')) == len(data_format)):
        print("Data len mismatch")
        return False
    else:
        for i, d in enumerate(data.split(',')):
            if not "NA" in d:
                result[data_format[i]] = type_converter(d, data_type[i])
            else:
                result[data_format[i]] = d

        return result


def get_timestamp() -> str:
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))



def receiving_thread(drawing_data: dict, warning_data: list, notes: dict, new_data: bool):
    # Serial Connection Module ----------
    serial_speed = 9600
    serial_port = '/dev/cu.usbserial-1130'

    ser = serial.Serial(serial_port, serial_speed, timeout=2)

    last_received_time = time.time()
    last_warning_time = time.time()

    last_packet = -1

    while True:

        # Try receiving data
        try:
            data = ser.readline().decode()
        except:
            data = False
            print(f'Invalid Data Received {data}')
        if data:
            if time.time() - last_received_time >= 2:
                print(f'interval {time.time() - last_received_time}')
                parsed = parse_data(data)
                if parsed:
                    print(parsed)
                    print(f'{parsed["latitude"]},{parsed["longitude"]}')
                    for key in parsed:
                        drawing_data[key] = parsed[key]

                    notes['interval'] = time.time() - last_received_time
                    if not parsed["latitude"] == 'NA':
                        notes['last_interval'] = parsed["latitude"]
                        notes['last_longitude'] = parsed["longitude"]
                    new_data.value = True
            last_received_time = time.time()


            # Check packet index
            if parsed != False:
                if parsed['packet_count'] - last_packet > 1 and not last_packet == -1:
                    print(f"Lost [{parsed['packet_count'] - last_packet}] Packets")
                    warning_data.append(get_timestamp() + f"Lost [{parsed['packet_count'] - last_packet}] Packets")
                    new_data.value = True
                last_packet = parsed['packet_count']


        if time.time() - last_received_time >= 5 and time.time() - last_warning_time >= 5:
            print("Connection Lost")
            warning_data.append(get_timestamp() + "Connection Lost")
            new_data.value = True
            last_warning_time = time.time()

if __name__ == '__main__':
    manager = Manager()

    drawing_data = manager.dict()
    warning_data = manager.list()
    notes = manager.dict()

    new_data = manager.Value('i', 0)
    new_data.value = 0

    p = Process(target=drawing_thread, args=(drawing_data, warning_data, notes, new_data,))
    p2 = Process(target=receiving_thread, args=(drawing_data, warning_data, notes, new_data,))

    p.start()
    p2.start()

    p.join()
    p2.join()
