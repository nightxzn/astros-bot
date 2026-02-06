import discord
from discord.ext import commands
from discord import app_commands

# ==========================
# CONFIG
# ==========================

OWNER_ID = 1357179231108464772  # coloque seu ID aqui

# ==========================
# VIEW (BOTÕES)
# ==========================

class PainelDonoView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    # botão reload cogs
    @discord.ui.button(label="🔄 Reload Cogs", style=discord.ButtonStyle.primary)
    async def reload_cogs(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("❌ Apenas o dono.", ephemeral=True)

        for ext in list(self.bot.extensions):
            await self.bot.reload_extension(ext)

        await interaction.response.send_message("✅ Cogs recarregadas.", ephemeral=True)

    # botão status
    @discord.ui.button(label="📊 Status", style=discord.ButtonStyle.success)
    async def status(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("❌ Apenas o dono.", ephemeral=True)

        guilds = len(self.bot.guilds)
        latency = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            f"🌍 Servidores: {guilds}\n🏓 Ping: {latency}ms",
            ephemeral=True
        )

# ==========================
# COG
# ==========================

class PainelDono(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="painel-dono", description="Painel exclusivo do dono")
    async def painel_dono(self, interaction: discord.Interaction):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "❌ Você não é o dono do Astros.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="⚡ Painel do Dono - Astros",
            description="Painel do dono - Only Dono",
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=PainelDonoView(self.bot),
            ephemeral=True
        )

# ==========================
# SETUP
# ==========================

async def setup(bot):
    await bot.add_cog(PainelDono(bot))
