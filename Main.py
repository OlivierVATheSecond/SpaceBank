import discord
from discord.ext.commands import bot
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import random
import json

#client setup
Client = discord.Client()
client = commands.Bot(command_prefix="")

#values
startball = 10000
cheque_book = {}

#startup sequence
@client.event
async def on_ready():
    print("Bank is ready")
    with open("cheque_book.json", "r") as f:
        global cheque_book
        cheque_book = json.load(f)

#message event handeler
@client.event
async def on_message(message):

    #check your ballance
    if message.content.lower() in ["!cs"]:
        uidn = message.author.name
        uid = message.author.id
        if cheque_book.get(uidn):
            await client.send_message(message.channel,"je saldo is: `$" + str(cheque_book.get(uidn)) + "`")
        else:
            await client.send_message(
                message.channel, "<@%s> je bent niet ingecheckt, gebruik: (!check in) om in te checken" % uid
            )

    #open account on your name
    if message.content.lower() in ["!check in", "!check-in"]:
        uidn = message.author.name
        uid = message.author.id
        if cheque_book.get(uidn):
            await client.send_message(message.channel, "<@%s> je bent al geregistreerd" % uid)
        else:
            cheque_book[uidn] = startball
            cheque_book["bank"] = cheque_book.get("bank") - float(startball)
            await client.send_message(
                message.channel, "<@%s> je bent ingecheckt, een basis saldo van `10.000` is gestort" % uid
            )

    #write from your account to someone else
    if message.content.lower().startswith("!os"):
        uidn = message.author.name
        uid = message.author.id
        args = message.content.split(" ")
        #print("msg got")
        amount = float(args[1])
        other_account = args[2]
        if amount > 0 and amount <= cheque_book.get(uidn) and other_account in cheque_book:
            print(args[1]+args[2])
            cheque_book[uidn] = cheque_book.get(uidn) - amount
            cheque_book[other_account] = cheque_book[other_account] + amount
            await client.send_message(message.channel, "je hebt " + "`" + str(amount) + "`" + " overgemaakt naar " +
                                      other_account + " je hebt nog" + "`" + str(cheque_book.get(uidn)) + "`" + " over."
            )
        else:
            await client.send_message(message.channel, "ongeldige trasactie")

    #dev command
    if message.content.lower() in ["!get_dict"]:
        await client.send_message(message.channel, cheque_book)

    #show commands
    if message.content.lower() in ["!help"]:
        await client.send_message(message.channel,
        "https://docs.google.com/document/d/1NWmTDV5A-jFSSOahNMUpYUKqjtZlvjHETU3By6j3E4k/edit?usp=sharing")

    #clear channel chat
    if message.content.lower() in ["!clear"]:
        limmit = 50
        messages = []
        async for message in client.logs_from(message.channel):
            messages.append(message)
        await client.delete_message(messages)

    #write from bank to account
    if message.content.lower().startswith("!bl"):
        uid = message.author.id
        args = message.content.split(" ")
        amount = float(args[1])
        other_account = args[2]
        if "485130136945950731" in [role.id for role in message.author.roles]:
            if other_account in cheque_book and amount > 0 and amount <= cheque_book.get("bank"):
                cheque_book[other_account] = cheque_book[other_account] + amount
                cheque_book["bank"] = cheque_book["bank"] - amount
                await client.send_message(message.channel, "je hebt " + "`" + str(amount) + "`" + " overgemaakt naar " +
                other_account )

        else:
            await client.send_message(message.channel, "dat commando is niet toegestaan!")

    #creates deposit account
    if message.content.lower().startswith("!cd"):
        if "485130136945950731" in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            cheque_book[str(args[1])] = {}
        else:
            await client.send_message(message.channel, "dat commando is niet toegestaan!")

    #deletes deposit account
    if message.content.lower().startswith("!vd"):
        if "485130136945950731" in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            del cheque_book[str(args[1])]
        else:
            await client.send_message(message.channel, "dat commando is niet toegestaan!")

    #write from to
    if message.content.lower().startswith("!svn"):
        args = message.content.split(" ")
        val = float(args[1])
        acc1 = str(args[2])
        acc2 = str(args[3])
        if "485130136945950731" in [role.id for role in message.author.roles] and val > 0 and acc1 != acc2:
            cheque_book[acc1] = cheque_book[acc1] - val
            cheque_book[acc2] = cheque_book[acc2] + val
        else:
            await client.send_message(message.channel, "ongeldige trasactie")

    #wrtite cheque_book to json file
    with open("cheque_book.json", "w") as f:
        json.dump(cheque_book, f)

#connect to client
client.run("NDg1MTE5NTA5MTgzNzI1NTY4.Dmsi_g.mWgm-MJGFKZv93QCYr3Y8_SSRPA")
