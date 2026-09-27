import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'📰 Бот новостей запущен как {bot.user.name}')

@bot.command(name='новость', help='Опубликовать новость. Использование: !новость Заголовок | Текст новости | URL_картинки(необязательно)')
@commands.has_permissions(administrator=True)
async def post_news(ctx, *, args: str):
    parts = [p.strip() for p in args.split('|')]
    
    title = parts[0]
    description = parts[1] if len(parts) > 1 else ""
    image_url = parts[2] if len(parts) > 2 else None

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.gold()
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    embed.set_footer(text="Официальные новости сервера")

    if image_url:
        embed.set_image(url=image_url)

    # Удаляем команду администратора
    await ctx.message.delete()

    # Отправляем красивый Embed
    news_message = await ctx.send(embed=embed)

    # Автоматически создаем ветку для обсуждений под новостью
    thread = await news_message.create_thread(
        name=f"💬 Обсуждение: {title[:50]}",
        auto_archive_duration=1440 # Автоархивация через 24 часа неактивности
    )
    await thread.send("Здесь можно оставить комментарии и обсудить данную новость!")

TOKEN ="rcDp-p0kf92_4DFkoYKlfZx3QY8Lqj23"
bot.run(TOKEN)
