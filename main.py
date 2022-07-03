# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
from turtle import st
import discord
import os

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.


@bot.event
async def on_ready():
    # Shows the bot's status in the console.
    print('Logged in as {}'.format(bot.user.name))


@bot.event
async def on_message(message):
    # Check stock ticker command.
    if message.content == "$checkstocks":
        # check stock in ./database
        stocks = []
        for stock in (os.listdir("./database/stocks")):
            # check value in files
            with open("./database/stocks/" + stock, "r") as f:
                # read value
                value = f.read()
                stocks.append(f'**{stock.split(".")[0]}** : **{value}**')
            
        quote = '\n'.join(stocks)
        quote_text = 'สินค้าที่เหลืออยู่ ล่าสุด:\n>>> {}'.format(quote)
        await (message.channel.send(quote_text))

    # set stocks
    if "$setstock hokkai" in message.content:
        data = message.content.split("!")
        try:
            number = int(data[1])
        except ValueError:
            number = None
        if number is not None and len(data) == 2:
            # open mamon and set
            open ("./database/stocks/hokkai.txt", "w").write(str(number))
        else:
            await (message.channel.send("Please enter a valid stock number."))

    if "$setstock butter" in message.content:
        data = message.content.split("!")
        try:
            number = int(data[1])
        except ValueError:
            number = None
        if number is not None and len(data) == 2:
            # open mamon and set
            open ("./database/stocks/butter.txt", "w").write(str(number))

        else:
            await (message.channel.send("Please enter a valid stock number."))
        
    if "$setstock mamon" in message.content:
        data = message.content.split("!")
        try:
            number = int(data[1])
        except ValueError:
            number = None
        if number is not None and len(data) == 2:
            # open mamon and set
            open ("./database/stocks/mamon.txt", "w").write(str(number))
        else:
            await (message.channel.send("Please enter a valid stock number."))
            


    # update stocks when receive message
    # if send from channel (order-มา)
    if message.channel.name == 'orders':
        embeds = message.embeds # return list of embeds
        embeds = embeds[0].to_dict() # it's content of embed in dict
        data = []
        label = ['name', 'place', 'phone', 'hokkai', 'butter', 'mamon', 'note']
        for each in embeds['fields']:
            data.append(each['value'])
        data = zip(label, data)
        data = dict(data) #sample {'name': 'test', 'place': 'test', 'phone': '0000000000', 'hokkai': '0', 'butter': '0', 'mamon': '0', 'note': 'test'}
        
        # open database and minus from current value
        # loop over list of db
        dblist = ['hokkai', 'butter', 'mamon']
        for db in dblist:
            with open("./database/stocks/" + db + ".txt", "r+") as f:
                value = f.read()
                try:
                    value = int(value) - int(data[db])
                    # write new value
                    f.seek(0)
                    f.writelines(str(value))
                    f.truncate()
                except ValueError:
                    print('Database Error Matafaka')
                    print(data[db])

                f.close()
                

        # update and send stocks
        # check stock in ./database
        stocks = []
        for stock in (os.listdir("./database/stocks")):
            # check value in files
            with open("./database/stocks/" + stock, "r") as f:
                # read value
                value = f.read()
                stocks.append(f'**{stock.split(".")[0]}** : **{value}**')
                f.close()
            
        quote = '\n'.join(stocks)
        quote_text = 'สินค้าที่เหลืออยู่ ล่าสุด:\n>>> {}'.format(quote)
        # send message to channel_id 992402846467239946 (quote_text)
        channel_id = 992402846467239946
        channel = bot.get_channel(channel_id)
        await channel.send(quote_text)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run("Token")
