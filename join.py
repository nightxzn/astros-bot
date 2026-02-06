import discord
from discord.ext import commands
from discord import app_commands

class Join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ==========================
    # SLASH COMMAND
    # ==========================

    @app_commands.command(name="join", description="Faz o Astros entrar na call (mudo e surdo)")
    async def join(self, interaction: discord.Interaction):

        # verificar se usuário está em call
        if not interaction.user.voice:
            return await interaction.response.send_message(
                "❌ Você precisa estar em uma call.",
                ephemeral=True
            )

        channel = interaction.user.voice.channel

        await interaction.response.defer()

        # entrar na call
        vc = await channel.connect()

        # ficar mudo e surdo (não escuta nem fala)
        await interaction.guild.change_voice_state(
            channel=channel,
            self_mute=True,
            self_deaf=True
        )

        await interaction.followup.send(
            f"✅ Entrei em {channel.mention}."
        )

# ==========================
# SETUP
# ==========================

async def setup(bot):
    await bot.add_cog(Join(bot))
