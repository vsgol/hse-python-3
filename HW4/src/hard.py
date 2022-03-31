import codecs
import time
from datetime import datetime
from multiprocessing import Queue, Pipe, Process


def worker_a(input_queue, output_pipe):
    while True:
        if not input_queue.empty():
            msg = input_queue.get()
            time.sleep(5)
            output_pipe.send(msg.lower())


def worker_b(input_pipe, output_queue):
    while True:
        output_queue.put(codecs.encode(input_pipe.recv(), 'rot_13'))


def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


if __name__ == '__main__':
    main_to_a = Queue()
    a_to_b, b_from_a = Pipe()
    b_to_main = Queue()
    Process(target=worker_a, args=(main_to_a, a_to_b), daemon=True).start()
    Process(target=worker_b, args=(b_from_a, b_to_main), daemon=True).start()

    message = ''
    with open('../artifacts/hard.txt', "w") as file:
        while True:
            while not b_to_main.empty():
                message = b_to_main.get()
                file.write(f'{current_time()} output "{message}"\n')
                print(message)
            try:
                message = input(">>> ")
            except EOFError:
                message = 'exit'
            if message == 'exit' or message == 'quit':
                while not b_to_main.empty() or not main_to_a.empty():
                    message = b_to_main.get()
                    file.write(f'{current_time()} output "{message}"\n')
                    print(message)
                file.write(f'{current_time()} end message\n')
                break
            main_to_a.put(message)
            file.write(f'{current_time()} input "{message}"\n')
