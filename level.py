import discord
from discord.ext import commands
import json
import time
import math

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "levels.json"
        self.cooldowns = {}  # anti spam (user_id: last_time)

        # cria arquivo se não existir
        try:
            with open(self.file, "r") as f:
                json.load(f)
        except:
            with open(self.file, "w") as f:
                json.dump({}, f)

    # =========================
    # Utils
    # =========================

    def load(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def get_level(self, xp):
        # fórmula básica
        return int(math.sqrt(xp) // 5)

    # =========================
    # XP por mensagem
    # =========================

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        now = time.time()
        user_id = str(message.author.id)

        # cooldown de 15s
        if user_id in self.cooldowns:
            if now - self.cooldowns[user_id] < 15:
                return

        self.cooldowns[user_id] = now

        data = self.load()

        if user_id not in data:
            data[user_id] = {"xp": 0}

        old_level = self.get_level(data[user_id]["xp"])

        # ganho XP
        data[user_id]["xp"] += 10

        new_level = self.get_level(data[user_id]["xp"])

        self.save(data)

        # aviso de level up
        if new_level > old_level:
            await message.channel.send(
                f"🎉 {message.author.mention} subiu para o nível **{new_level}**!"
            )

    # =========================
    # Comando rank
    # =========================

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):

        member = member or ctx.author
        data = self.load()

        user_id = str(member.id)

        if user_id not in data:
            return await ctx.send("Usuário sem XP ainda.")

        xp = data[user_id]["xp"]
        level = self.get_level(xp)

        embed = discord.Embed(
            title=f"Rank de {member}",
            color=discord.Color.blue()
        )

        embed.add_field(name="Nível", value=level)
        embed.add_field(name="XP", value=xp)

        await ctx.send(embed=embed)

    # =========================
    # Leaderboard
    # =========================

    @commands.command()
    async def leaderboard(self, ctx):

        data = self.load()

        sorted_users = sorted(
            data.items(),
            key=lambda x: x[1]["xp"],
            reverse=True
        )

        desc = ""

        for i, (user_id, info) in enumerate(sorted_users[:10]):
            user = self.bot.get_user(int(user_id))
            name = user.name if user else f"ID {user_id}"
            desc += f"**{i+1}.** {name} — {info['xp']} XP\n"

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description=desc,
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Level(bot))
