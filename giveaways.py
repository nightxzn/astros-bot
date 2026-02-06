import discord
from discord.ext import commands
from discord import app_commands
import random

class GiveawayView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.participantes = []

    @discord.ui.button(label="Participar 🎉", style=discord.ButtonStyle.green)
    async def participar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user in self.participantes:
            await interaction.response.send_message(
                "Você já entrou!",
                ephemeral=True
            )
            return

        self.participantes.append(interaction.user)
        await interaction.response.send_message("Você entrou no sorteio!", ephemeral=True)


class Giveaways(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sorteio", description="Criar sorteio")
    async def sorteio(self, interaction: discord.Interaction, premio: str):

        view = GiveawayView()

        embed = discord.Embed(
            title="🎁 Sorteio",
            description=f"Prêmio: **{premio}**\nClique para participar!",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
