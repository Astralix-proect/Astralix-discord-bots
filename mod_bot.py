import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Список запрещенных слов для автомодерирования
BAD_WORDS = ["спам_слово1", "плохое_слово2"]

@bot.event
async def on_ready():
    print(f'🛡️ Бот модерации запущен как {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Фильтр запрещенных слов
    for word in BAD_WORDS:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}, ваше сообщение содержит запрещенные слова!', delete_after=5)
            return

    await bot.process_commands(message)

@bot.command(name='кик', help='Удалить пользователя с сервера')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Причина не указана"):
    await member.kick(reason=reason)
    await ctx.send(f'👢 Пользователь {member.mention} кикнут. Причина: {reason}')

@bot.command(name='бан', help='Забанить пользователя')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Причина не указана"):
    await member.ban(reason=reason)
    await ctx.send(f'⛔ Пользователь {member.mention} забанен. Причина: {reason}')

@bot.command(name='разбан', help='Разбанить пользователя по ИМЕНИ#ТЕГУ')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name: str):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == tuple(member_name.split('#')):
            await ctx.guild.unban(user)
            await ctx.send(f'✅ Пользователь {user.mention} разбанен.')
            return
    await ctx.send("Пользователь не найден в списке банов.")

@bot.command(name='очистить', help='Удалить N сообщений')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f'🧹 Удалено {amount} сообщений.', delete_after=5)

TOKEN = "ТВОЙ_ТОКЕН_БОТА_МОДЕРАЦИИ"
bot.run(TOKEN)
