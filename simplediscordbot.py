#(1) greet a newly joined member in a channel (random message) ........................done
#(2) while adding a reaction to a message send a message to a channel (<user> gave reaction to <user>)
#(3) parameterized command, create a role named the parameter recieved and assign it to the user.
#(4) using a parameterized command(eg - !register <name>) insert the name to database, if same name
# tries to register again send error message to channel.
#(5) with a role restricted command retrieve all names in the database ( eg - !names)


import discord
from discord.ext import commands
import sqlite3


TOKEN = "ODE3MDg5NTA2MjIxMDk3MDYy.YEEb5w.vZxH46phdu79ADLU2T0Zk29bTBc"
intents = discord.Intents.all()
intents.reactions = True
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@client.event
async def on_ready():
    db=sqlite3.connect("discord_database.sqlite")
    cursor= db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discord(
        name TEXT NOT NULL PRIMARY KEY
        )
    ''')

    print(f"BOT {client.user} IS ONLINE")

@client.command()
async def reg(ctx, name):
    db=sqlite3.connect("discord_database.sqlite")
    cursor = db.cursor()
    cursor.execute('''
    SELECT name
    FROM discord
    WHERE name=?
    ''',
    (name,)
    )

    result=cursor.fetchone()

    if result:
        await ctx.send(f"{name} is already registered")
    else:
        cursor.execute("INSERT INTO discord VALUES(?)",(name,))
        db.commit()
        await ctx.send(f"{name} has been registered")

@client.command()
async def names(ctx):
    db=sqlite3.connect("discord_database.sqlite")
    cursor = db.cursor()
    result=cursor.fetchone()
    cursor.execute("SELECT * FROM discord")
    rows=cursor.fetchall()
    for i in rows:
        await ctx.send(i)


@client.command()
async def help(context):
    await context.send('''
    WELCOME TO ANAND'S BOT:
    
    ROLES:
        Admin
        player1
        player2
    
    TO ADD ROLE:
        !add_role role username
    TO REMOVE ROLE:
        !remove_role role username
    
    TO REGISTER YOUR NAME:
        !reg username
    
    TO SHOW ALL NAMES IN DATABASE:
        !names
        
    
    
    
    ''')



@client.event
async def on_member_join(member):
    channel = client.get_channel(816361007101771799)
    await channel.send(f"WELCOME {member.name} . Enter !help to know more")


@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(816361007101771799)
    msg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    author = msg.author
    await channel.send(f"{payload.member} REACTED TO {author}'s MESSAGE")



@client.command()
async def add_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f"given role to {role.mention} to {user.mention}")

@client.command()
async def remove_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f"removed role {role.mention} of {user.mention}")


client.run(TOKEN)