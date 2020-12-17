import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import random
import time

description = '''Lilin Bot'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



@bot.command()
async def spam(ctx, times: int, content='repeating...'):
    user = ctx.message.author
    """Spammt den Channel mit einer Nachricht voll."""
    for i in range(times):
        await ctx.send(content)

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?spam", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def info(ctx, member: discord.Member):
    user = ctx.message.author
    mention = []
    for role in member.roles:
        if role.name != "@everyone":
            mention.append(role.mention)

    embedVar = discord.Embed(title=member.display_name, description=f"Discord ID: {member.id}", color=0x00ff00)
    embedVar.add_field(name="Server beigetreten", value=member.joined_at, inline=False)
    embedVar.add_field(name="User Rollen", value=mention, inline=False)
    embedVar.add_field(name="Profilbild", value=f"{member.avatar_url}", inline=False)
    embedVar.set_image(url=(member.avatar_url))
    await ctx.send(embed=embedVar)

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?info", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def ha_set(ctx, text: str):
    user = ctx.message.author
    """Mit diesem Befehl werden Hausaufgaben gespeichert."""
    text_file = open("Output.txt", "w")
    text_file.write(text)
    text_file.close()

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?ha_set", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def ha(ctx):
    user = ctx.message.author
    """Ruft die aktuellen Hausaufgaben ab."""
    try:
        ha_channel = discord.utils.get(ctx.guild.text_channels, name="⥤hausaufgaben⥢")
        ha_channel_id = ha_channel.id
        ha_ch = bot.get_channel(ha_channel_id)
        text_file = open("Output.txt", "r")
        await ha_ch.send("**Aktuelle Hausaufgaben**")
        await ha_ch.send(text_file.read())
        text_file.close()
    except Exception:
        await ctx.send("Der Channel -hausaufgaben- existiert nicht. Führe zuerst bitte -?setup- aus.")

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?ha", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def ha_clear(ctx):
    user = ctx.message.author
    """Löscht den Inhalt der Hausaufgaben Liste."""
    text_file = open("Output.txt", "r+")
    text_file.truncate(0)
    text_file.close()

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?ha_clear", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def clear(ctx, amount=None):
    user = ctx.message.author
    """Löscht Nachrichten im Channel."""
    if amount is None:
        await ctx.channel.purge(limit=5)
    elif amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount))

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?clear", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def help(ctx):
    user = ctx.message.author
    embedVar = discord.Embed(title="Hilfe Seite", description="Hier findest du alle Befehle.", color=0xFF0000)
    embedVar.add_field(name="?spam", value="Spammt den Channel mit einer Nachricht voll. - ?spam 4 NACHRICHT", inline=False)
    embedVar.add_field(name="?info", value="Gibt dir Informationen eines Users. - ?info @USER", inline=False)
    embedVar.add_field(name="?clear", value="Löscht Nachrichten in einem Channel. - ?clear (all oder ANZAHL)", inline=False)
    await ctx.send(embed=embedVar)

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?help", inline=False)
    await log_channel.send(embed=logVar)


@bot.command()
async def server(ctx):
    user = ctx.message.author
    mention = []
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            mention.append(role.mention)

    embedVar = discord.Embed(title="Server Information", description="Informationen über den Server.", color=0xFF0000)
    embedVar.set_thumbnail(url=(str(ctx.guild.icon_url)))
    embedVar.add_field(name="Server ID", value=ctx.guild.id, inline=True)
    embedVar.add_field(name="Server Name", value=ctx.guild.name, inline=True)
    embedVar.add_field(name="Server Besitzer", value=ctx.guild.owner, inline=False)
    embedVar.add_field(name="Anzahl der User", value=ctx.guild.member_count, inline=False)
    embedVar.add_field(name="Text Channel", value=(len(ctx.guild.text_channels)), inline=True)
    embedVar.add_field(name="Voice Channel", value=(len(ctx.guild.voice_channels)), inline=True)
    embedVar.add_field(name="Rollen", value=mention, inline=False)
    embedVar.add_field(name="Erstellt am", value=ctx.guild.created_at, inline=False)
    await ctx.send(embed=embedVar)

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?server", inline=False)

    await log_channel.send(embed=logVar)
    #await log_channel.send(f"{ctx.message.author} - {ctx.message.created_at}, ?server wurde ausgeführt.")



@bot.command()
async def setup(ctx):
    user = ctx.message.author
    if ctx.message.author.guild_permissions.administrator:
        await ctx.guild.create_category("ITA", position=1)
        category = discord.utils.get(ctx.guild.channels, name="ITA")
        category_id = category.id

        await ctx.guild.create_text_channel("⥤Hausaufgaben⥢", category=(bot.get_channel(category_id)))
        await ctx.guild.create_text_channel("⥤Klassenarbeiten⥢", category=(bot.get_channel(category_id)))
        await ctx.guild.create_text_channel("bot-log", category=(bot.get_channel(category_id)))
        time.sleep(2)
        ha_channel = discord.utils.get(ctx.guild.text_channels, name="⥤hausaufgaben⥢")
        ka_channel = discord.utils.get(ctx.guild.text_channels, name="⥤klassenarbeiten⥢")
        log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
        
        await log_channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
        await ctx.send(f"Setup wurde erfolgreich ausgeführt. {ha_channel.mention}, {ka_channel.mention}")

        log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
        logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
        logVar.set_thumbnail(url=(user.avatar_url))
        logVar.add_field(name="User", value=ctx.message.author, inline=False)
        logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
        logVar.add_field(name="Befehl", value="?setup", inline=False)
        await log_channel.send(embed=logVar)
    else:
        await ctx.send("Du hast nicht genug Rechte um dies zu tun.")



@bot.command()
async def rename(ctx, member: discord.Member, name):
    user = ctx.message.author
    await member.edit(nick=name)
    await ctx.send(f'Name wurde geändert.')

    log_channel = discord.utils.get(ctx.guild.text_channels, name="bot-log")
    logVar = discord.Embed(title="Log", description="Befehlslog", color=0xFF0000)
    logVar.set_thumbnail(url=(user.avatar_url))
    logVar.add_field(name="User", value=ctx.message.author, inline=False)
    logVar.add_field(name="Uhrzeit", value=ctx.message.created_at, inline=False)
    logVar.add_field(name="Befehl", value="?rename", inline=False)
    await log_channel.send(embed=logVar)

@bot.command()
async def announce(ctx, message):
    news_channel = discord.utils.get(ctx.guild.text_channels, name="⌠🔔⌡news")
    await news_channel.send(message)





bot.run('TOKEN')
