import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import datetime

load_dotenv()

TOKEN = os.getenv('TOKEN')

# CAMBIA ESTOS DOS IDs por los de tu servidor (usa modo desarrollador en Discord para copiarlos)
WELCOME_CHANNEL_ID = 123456789012345678  # ID del canal donde van las bienvenidas
AUTO_ROLE_ID = 123456789012345678        # ID del rol que se da al entrar

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} está en línea y listo!')
    await bot.change_presence(activity=discord.Game(name="!help | NovaMod"))

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"¡Bienvenido {member.name}! 👋",
            description=f"¡Bienvenido {member.mention} a **{member.guild.name}**! 🎉\nDisfruta tu estancia y lee las reglas.",
            color=0x00ff88
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Ahora somos {member.guild.member_count} miembros")
        await channel.send(embed=embed)

        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            await member.add_roles(role)

# Moderación
@bot.command()
@commands.has_permissions(kick_members=True)
async def expulsar(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} ha sido expulsado.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def banear(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} ha sido baneado.')

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason=None):
    await member.timeout(datetime.timedelta(minutes=minutes), reason=reason)
    await ctx.send(f'{member.mention} tiene timeout de {minutes} minutos.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Se borraron {amount} mensajes.', delete_after=5)

# Comandos divertidos
@bot.command(name='8ball')
async def eightball(ctx, *, pregunta):
    respuestas = ["Sí", "No", "Tal vez", "¡Claro que sí!", "Ni de broma", "Pregunta de nuevo"]
    await ctx.send(f"🎱 {random.choice(respuestas)}")

@bot.command()
async def abrazar(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention} abrazó a {member.mention} 💕")

@bot.command()
async def golpear(ctx, member: discord.Member):
    await ctx.send(f"👊 {ctx.author.mention} le dio un golpe a {member.mention} 😂")

@bot.command()
async def decir(ctx, *, texto):
    await ctx.message.delete()
    await ctx.send(texto)

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 ¡Pong! Latencia: {round(bot.latency * 1000)}ms')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Comandos de NovaMod", color=0x00ff88)
    embed.add_field(name="Moderación", value="!expulsar @user | !banear @user | !timeout @user minutos | !limpiar cantidad", inline=False)
    embed.add_field(name="Diversión", value="!8ball pregunta | !abrazar @user | !golpear @user | !decir texto | !ping", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
