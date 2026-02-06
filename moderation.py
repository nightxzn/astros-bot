import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Banir usuário")
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str="Sem motivo"):

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Sem permissão.", ephemeral=True)
            return

        await membro.ban(reason=motivo)
        await interaction.response.send_message(f"{membro} foi banido.")

    @app_commands.command(name="kick", description="Expulsar usuário")
    async def kick(self, interaction: discord.Interaction, membro: discord.Member):

        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("Sem permissão.", ephemeral=True)
            return

        await membro.kick()
        await interaction.response.send_message(f"{membro} foi expulso.")

    @app_commands.command(name="clear", description="Limpar mensagens")
    async def clear(self, interaction: discord.Interaction, quantidade: int):

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Sem permissão.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=quantidade)
        await interaction.followup.send(f"{quantidade} mensagens apagadas.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
