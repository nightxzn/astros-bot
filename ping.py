import discord
from discord.ext import commands
from discord import app_commands
import time
import asyncio

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ==========================
    # BARRA VISUAL
    # ==========================

    def barra_ping(self, ping):

        if ping <= 80:
            return "🟩🟩🟩🟩🟩"
        elif ping <= 150:
            return "🟨🟨🟨🟨⬜"
        elif ping <= 300:
            return "🟧🟧🟧⬜⬜"
        else:
            return "🟥🟥⬜⬜⬜"

    # ==========================
    # NIVEL LATENCIA
    # ==========================

    def nivel_ping(self, ping):

        if ping <= 80:
            return "🟢 Ultra rápido"
        elif ping <= 150:
            return "🟡 Boa"
        elif ping <= 300:
            return "🟠 Média"
        else:
            return "🔴 Ruim"

    # ==========================
    # CORE PING SYSTEM
    # ==========================

    async def executar_ping(self, ctx=None, interaction=None):

        # animação inicial
        if interaction:
            await interaction.response.send_message("🏓 Calculando latência...")
            msg = await interaction.original_response()
        else:
            msg = await ctx.send("🏓 Calculando latência...")

        # websocket latency
        ws_latency = round(self.bot.latency * 1000)

        # medir API real (tempo edit mensagem)
        samples = []

        for i in range(3):
            start = time.perf_counter()
            await msg.edit(content=f"🏓 Medindo API... ({i+1}/3)")
            end = time.perf_counter()

            api_time = (end - start) * 1000
            samples.append(api_time)

            await asyncio.sleep(0.3)

        api_latency = round(sum(samples) / len(samples))

        # jitter (variação entre samples)
        jitter = round(max(samples) - min(samples))

        # latency final
        final_latency = round((ws_latency + api_latency) / 2)

        # detectar lag spike
        lag_spike = "❌ Não"
        if jitter > 100:
            lag_spike = "⚠️ Detectado"

        # embed final
        embed = discord.Embed(
            title="🚀 Astros  Ping",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="WebSocket",
            value=f"{ws_latency}ms {self.barra_ping(ws_latency)}",
            inline=False
        )

        embed.add_field(
            name="API Latency",
            value=f"{api_latency}ms {self.barra_ping(api_latency)}",
            inline=False
        )

        embed.add_field(
            name="Jitter",
            value=f"{jitter}ms",
            inline=True
        )

        embed.add_field(
            name="Lag Spike",
            value=lag_spike,
            inline=True
        )

        embed.add_field(
            name="Final",
            value=f"{final_latency}ms — {self.nivel_ping(final_latency)}",
            inline=False
        )

        embed.set_footer(text="Essa é minha latência final!")

        await msg.edit(content=None, embed=embed)

    # ==========================
    # PREFIX
    # ==========================

    @commands.command(name="ping")
    async def ping_prefix(self, ctx):
        await self.executar_ping(ctx=ctx)

    # ==========================
    # SLASH
    # ==========================

    @app_commands.command(name="ping", description="Ping ultra avançado do Astros")
    async def ping_slash(self, interaction: discord.Interaction):
        await self.executar_ping(interaction=interaction)

# ==========================
# SETUP
# ==========================

async def setup(bot):
    await bot.add_cog(Ping(bot))
