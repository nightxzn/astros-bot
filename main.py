import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# ==========================
# LOAD ENV
# ==========================

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

# ==========================
# INTENTS
# ==========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ==========================
# BOT CLASS
# ==========================

class AstrosBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        print("🔄 Astros carregando cogs...")

        # auto load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregado: {filename}")

        # sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"🌍 Slash commands sincronizados: {len(synced)}")
        except Exception as e:
            print(f"❌ Erro ao sincronizar slash: {e}")

# ==========================
# INIT BOT
# ==========================

bot = AstrosBot()

# ==========================
# READY
# ==========================

@bot.event
async def on_ready():
    print(f"\n🚀 Astros conectado como {bot.user}")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="A Escuridão, é o melhor lugar pra mim.....")
    )

# ==========================
# INFO LOG (PREFIX COMMANDS)
# ==========================

@bot.event
async def on_command(ctx):
    print(f"[INFO] alguém usou o comando: {ctx.command}")

# ==========================
# INFO LOG (SLASH COMMANDS)
# ==========================

@bot.event
async def on_app_command_completion(interaction, command):
    print(f"[INFO] alguém usou o comando: {command.name}")

# ==========================
# ERROR LOG (PREFIX)
# ==========================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return

    arquivo = (
        ctx.command.cog.__class__.__name__
        if ctx.command and ctx.command.cog
        else "Desconhecido"
    )

    print(f"[ERRO] Astros detectou algum erro em ({arquivo})")
    print(error)

# ==========================
# ERROR LOG (SLASH)
# ==========================

@bot.tree.error
async def on_app_command_error(interaction, error):

    comando = (
        interaction.command.name
        if interaction.command
        else "Desconhecido"
    )

    print(f"[ERRO] Astros detectou algum erro em ({comando})")
    print(error)

# ==========================
# RUN
# ==========================

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
