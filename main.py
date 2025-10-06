import os
import discord
import logging
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(
    mongo_uri)

intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')

temp = mongo_client.list_database_names()
db = mongo_client['Bot']
collection = db['Saber']


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        string = message.content
        if 'gif' in string and 'saber' in string and message.author.id == 450082856417361920:
            doc = collection.find_one({'_id': ObjectId('68d9d971d6cee9f36b1e8e64')})
            prev = doc['day_count']
            prev += 1

            collection.update_one(
                {'_id': ObjectId('68d9d971d6cee9f36b1e8e64')},
                {'$set': {'day_count': prev}}
            )      
            await message.reply(prev)

client = MyClient(intents=intents)
client.run(discord_token, log_handler=handler)