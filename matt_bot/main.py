import discord
from discord.ext import tasks, commands
from forex_python.converter import CurrencyRates
import asyncio

id_file = open('./priv/client_id', 'r')
channel_id = int(id_file.readline())
id_file.close()

def get_rate():
    c = CurrencyRates()
    return c.convert('USD', 'JPY', .25)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()

async def update():
    await client.wait_until_ready()
    while True:
        print('ready')
        ch = client.get_channel(channel_id)
        print(ch.name)
        out = 'Current exchange rate of 0.25 USD to JPY: ' + str(get_rate()) + '円'
        await ch.send(content=out)
        new_name = str(get_rate()) + '円'
        for role in ch.guild.roles:
            if role.name == 'matt':
                for member in role.members:
                    await member.edit(nick=new_name)
        await asyncio.sleep(1800)

client.loop.create_task(update())

code_file = open('./priv/code', 'r')
client.run(code_file.readline())
code_file.close()

