import discord
from discord.ext import commands
import pymysql
import logging

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'discord_bot',
}

# Initialize Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

# Global variables for database connection
db_conn = None
db_cursor = None

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    global db_conn, db_cursor 
    print(f'Logged in as {bot.user.name}')
    
    try:
        db_conn = pymysql.connect(**db_config)
        db_cursor = db_conn.cursor()

        channel_id = 1184552195451015300
        channel = bot.get_channel(channel_id)
        
        if channel:
            print(f'Found channel: {channel.name} (ID: {channel.id})')
            await channel.send(f'Hello! I am now connected as {bot.user.name}')
        else:
            print(f"Error: Channel with ID {channel_id} not found.")

    except pymysql.Error as err:
        print(f"Error connecting to the database: {err}")


@bot.command(name='hello')
async def hello(ctx):
    global db_cursor

    print("Hello command executed!")

    if ctx.guild is None:
        print("Error: Command cannot be used in private messages. Please use it in a server.")
        await ctx.send('This command cannot be used in private messages. Please use it in a server.')
        return

    server_id = ctx.guild.id
    print(f"Server ID: {server_id}")

    try:
        db_cursor.execute('SELECT * FROM auth_tokens WHERE server_id = %s', (server_id,))
        result = db_cursor.fetchone()
        print(f"Database Query Result: {result}")

        if result:
            await ctx.send(f'Hello World! This is {ctx.guild.name}')
        else:
            await ctx.send('Unauthorized. Please authenticate the bot in this server.')

    except Exception as e:
        print(f"Error in database query: {e}")
        await ctx.send('An error occurred. Please try again later.')

# Run the bot
if __name__ == '__main__':
    bot.run('MTE4NDU0MjAwMjI4MTQ0NzU1Ng.GFg-wK.WHzMUu_-fTkuCx97t2R_hNtcW0hRRa1rhTZdt4')
