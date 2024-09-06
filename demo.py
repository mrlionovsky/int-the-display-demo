#Demo: Int The Display
#Code: Lionovsky
#Music: 4MAT

import subprocess
import threading
import time
import serial
import pyaudio
import numpy as np
import random
import psutil
import getpass
from datetime import datetime

def send_to_display(text, port='COM4', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            ser.write(b'\x0C')  # Очистка дисплея
            ser.write(text[:20].encode('cp866').ljust(20))
    except serial.SerialException:
        print(f"Error: Could not open port {port}")

def get_sound_level():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    volume = np.linalg.norm(data) / CHUNK
    stream.stop_stream()
    stream.close()
    p.terminate()
    return volume

def scroll_text_left(text, width=20, delay=0.3):
    display_text = ' ' * width + text
    for i in range(len(display_text) - width + 1):
        send_to_display(display_text[i:i+width])
        time.sleep(delay)

def scroll_text_right(text, width=20, delay=0.1):
    display_text = text + ' ' * width
    for i in range(len(display_text) - width + 1):
        send_to_display(display_text[-(i+width):-i] if i != 0 else display_text[-width:])
        time.sleep(delay)

def fade_out_text(text, delay=0.1):
    for i in range(len(text) + 1):
        send_to_display(text[:len(text) - i].ljust(20))
        time.sleep(delay)

def fade_in_text(text, delay=0.1):
    for i in range(len(text) + 1):
        send_to_display(text[:i].ljust(20))
        time.sleep(delay)

def random_case_text(text, iterations=10, delay=0.3):
    for _ in range(iterations):
        random_text = ''.join(random.choice([c.upper(), c.lower()]) for c in text)
        send_to_display(random_text.ljust(20))
        time.sleep(delay)
        
def scroll_text_once(text, width=20, delay=0.1):
    display_text = ' ' * width + text + ' ' * width
    for i in range(len(display_text) - width + 1):
        send_to_display(display_text[i:i+width])
        time.sleep(delay)

def display_emoticons(emoticons, delay=0.1):
    for emoticon in emoticons:
        send_to_display(emoticon.ljust(20))
        time.sleep(delay)
        
def random_case_info(iterations=10, delay=0.3):
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    info_text = f"CPU: {cpu_usage}% RAM: {ram_usage}%"
    
    for _ in range(iterations):
        random_text = ''.join(random.choice([c.upper(), c.lower()]) for c in info_text)
        send_to_display(random_text.ljust(20))
        time.sleep(delay)
        
def fade_out_info(delay=0.2):
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    info_text = f"CPU: {cpu_usage}% RAM: {ram_usage}%"
    
    for i in range(len(info_text) + 1):
        send_to_display(info_text[:len(info_text) - i].ljust(20))
        time.sleep(delay)

def get_network_usage_percentage():
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    total_bytes = bytes_sent + bytes_recv
    return total_bytes

def blink_text(text, iterations=10, delay=0.3):
    for _ in range(iterations):
        send_to_display(text.ljust(20))
        time.sleep(delay)
        send_to_display(' ' * 20)  # Очистка дисплея
        time.sleep(delay)

def display_network_usage_blink(iterations=10, delay=0.3):
    initial_bytes = get_network_usage_percentage()
    time.sleep(1)  # Задержка для измерения изменения
    final_bytes = get_network_usage_percentage()
    network_usage = final_bytes - initial_bytes
    info_text = f"Net: {network_usage}B/s"
    
    blink_text(info_text, iterations, delay)

def greet_user():
    username = getpass.getuser()
    message = f"{username}!"
    send_to_display(message)

def rolling_ball_attack(width=20, min_delay=0.05, max_delay=0.2, repetitions=3):
    ball = 'O'
    empty_space = ' ' * (width - 1)
    
    for _ in range(repetitions):
        # Случайное положение буквы (врага)
        enemy_position = random.randint(1, width - 2)
        enemy = chr(random.randint(65, 90))  # Случайная буква от A до Z
        
        # Движение шарика к врагу
        for i in range(enemy_position + 1):
            display_text = empty_space[:i] + ball + empty_space[i:]
            send_to_display(display_text[:width])
            time.sleep(random.uniform(min_delay, max_delay))
        
        # Удар по врагу
        display_text = empty_space[:enemy_position] + ball + enemy + empty_space[enemy_position + 1:]
        send_to_display(display_text[:width])
        time.sleep(0.5)
        
        # Удаление врага
        display_text = empty_space[:enemy_position] + ball + empty_space[enemy_position + 1:]
        send_to_display(display_text[:width])
        time.sleep(0.5)
        
        # Возвращение шарика на исходную позицию
        for i in range(enemy_position, -1, -1):
            display_text = empty_space[:i] + ball + empty_space[i:]
            send_to_display(display_text[:width])
            time.sleep(random.uniform(min_delay, max_delay))

def snake_movement(width=20, delay=0.1):
    snake = ['@']
    empty_space = ' ' * (width - 1)
    
    while len(snake) < width:
        for i in range(width):
            display_text = empty_space[:i] + ''.join(snake) + empty_space[i:]
            send_to_display(display_text[:width])
            time.sleep(delay)
            if len(snake) < width:
                snake.append('@')
            else:
                break

def volleyball_game(width=20, delay=0.1, repetitions=2):
    player1 = 'A'
    player2 = 'B'
    ball = 'O'
    empty_space = ' ' * (width - 2)
    
    for _ in range(repetitions):
        # Мяч летит от игрока 1 к игроку 2
        for i in range(1, width - 1):
            display_text = player1 + empty_space[:i-1] + ball + empty_space[i:] + player2
            send_to_display(display_text[:width])
            time.sleep(delay)
        
        # Мяч летит от игрока 2 к игроку 1
        for i in range(width - 2, 0, -1):
            display_text = player1 + empty_space[:i-1] + ball + empty_space[i:] + player2
            send_to_display(display_text[:width])
            time.sleep(delay)

def display_sound_level():
    GAIN = 1  # Коэффициент усиления
    symbols = ["=", "-", "@", "O"]  # Список символов для случайной смены
    last_info_time = time.time()
    last_cpu_ram_time = time.time()
    last_datetime_time = time.time()
    start_time = time.time()

    while True:
        volume = get_sound_level()
        level = int((volume * GAIN) / 20)  # Преобразование уровня звука в количество символов с усилением
        chosen_symbol = random.choice(symbols)  # Выбор случайного символа
        display_text = chosen_symbol * min(level, 20)  # Отображение уровня звука выбранным символом
        send_to_display(display_text)

        current_time = time.time()

        if current_time - start_time >= 8 and current_time - start_time < 10:
            fade_in_text("Int the Display")
            time.sleep(2)

        if current_time - start_time >= 14 and current_time - start_time < 15:
            fade_in_text("It's demo running on")
            time.sleep(0.5)
            fade_in_text("CD-7220 Display.")
            time.sleep(1)
            scroll_text_right("Perfect!")
            time.sleep(2)

        if current_time - start_time >= 30 and current_time - start_time < 35:
            scroll_text_once("This is really cool. Just check out this scrolling text!!!")
            time.sleep(1)
            random_case_text("Duck are best")
            random_case_text("Teapods too.")
            time.sleep(1)
        if current_time - start_time >= 54 and current_time - start_time < 62:
            emoticons_list = [":-)", ":-)", ":3", ":-@", ":-E", "o_O", "O_O", "O_o", "o_O", "O_O", "O_o", ":^)", ":>)", ":^)))"]
            display_emoticons(emoticons_list)
            random_case_text("Hmm... I know...")
            random_case_text("...about you...")
            time.sleep(0.5)
            fade_out_info()
            random_case_text("Replay!")
            random_case_info()
            random_case_text("and...")
            display_network_usage_blink()
            greet_user()
            time.sleep(3)
            random_case_text("You are best! <3")
            time.sleep(2)
            display_emoticons(emoticons_list)
            display_emoticons(emoticons_list)
            
        if current_time - start_time >= 108 and current_time - start_time < 130:
            scroll_text_once("MS DOS v 6.6.6. Loading...")
            time.sleep(1)
            scroll_text_once("LOADED!")
            time.sleep(0.5)
            scroll_text_left("D:")
            time.sleep(0.5)
            scroll_text_left("CD GAME")
            time.sleep(0.5)
            scroll_text_left("game.com")
            time.sleep(0.5)
            rolling_ball_attack()
            time.sleep(2)
            scroll_text_left("CD ..")
            time.sleep(0.5)
            scroll_text_left("snake/snake.exe")
            time.sleep(0.5)
            snake_movement()
            time.sleep(0.5)
            scroll_text_left("vb/vb.exe")
            time.sleep(0.5)
            volleyball_game()
            time.sleep(0.5)
            scroll_text_left("shutdown -h now")
            time.sleep(0.5)
            scroll_text_once("This DEMO can be closed.")
            time.sleep(3)
            random_case_text("ABOUT")
            time.sleep(2)
            scroll_text_once("Music: In the Kitchen by 4mat. Code: Lionovsky. lionovsky.us, 2024")
            time.sleep(0.5)
            scroll_text_once("$username$. Once again, you are the best. :3")
            time.sleep(2)
            

def play_audio():
    subprocess.run(['python', 'audio.py'])

def main():
    # Запуск аудио в фоновом режиме
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

    display_thread = threading.Thread(target=display_sound_level)
    display_thread.start()

    display_thread.join()

if __name__ == "__main__":
    main()
