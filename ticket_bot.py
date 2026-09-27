import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Закрыть тикет", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Канал будет удален через 5 секунд...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Открыть тикет", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Проверка, нет ли уже тикета у этого пользователя
        channel_name = f"ticket-{user.name}".lower().replace(" ", "-")
        existing_channel = discord.utils.get(guild.channels, name=channel_name)

        if existing_channel:
            await interaction.response.send_message(f"У вас уже открыт тикет: {existing_channel.mention}", ephemeral=True)
            return

        # Настройка прав доступа для приватного канала
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        embed = discord.Embed(
            title="🎟️ Тикет создан",
            description=f"Здравствуйте, {user.mention}! Напишите ваш вопрос или проблему. Администрация ответит вам в ближайшее время.",
            color=discord.Color.green()
        )
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"Тикет успешно создан: {channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
    print(f'🎟️ Бот тикетов запущен как {bot.user.name}')

@bot.command(name='тикет_меню', help='Отправить панель для создания тикетов')
@commands.has_permissions(administrator=True)
async def setup_tickets(ctx):
    embed = discord.Embed(
        title="Поддержка и Связь с Администрацией",
        description="Нажмите на кнопку ниже, чтобы открыть приватный тикет и задать вопрос.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())

TOKEN = "ТВОЙ_ТОКЕН_БОТА_ТИКЕТОВ"
bot.run(TOKEN)
