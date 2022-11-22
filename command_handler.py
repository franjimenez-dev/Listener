import asyncio
import random

from command_list import command_list
from animegifs import animegifs

from youtube import Player


class CommandHandler:
    commandList = []

    def __init__(self, bot):
        self.ctx = None
        self.bot = bot
        for command in command_list:
            self.commandList.append(command)

    async def check_command(self, prompt, ctx):
        self.ctx = ctx
        prompt = prompt.lower()
        print(prompt)
        if prompt != "":
            youtube_case = prompt.find("youtube")
            print(youtube_case)
            if youtube_case >= 0:
                await self.youtube(prompt)
                return True
            else:
                spotify_case = prompt.find("spotify")
                if spotify_case >= 0:
                    self.spotify(prompt)
                    return True
                else:
                    cats_case = prompt.find("cats")
                    if cats_case >= 0:
                        self.cats(ctx)
                        return True
                    else:
                        anime_case = prompt.find("anime")
                        if anime_case >= 0:
                            await self.anime(prompt, ctx)
                            return True
                        else:
                            print("nothing")
                            return False
        else:
            print("nothing")
            return False

    async def youtube(self, prompt):

        index = prompt.find("youtube")
        index += len("youtube") + 1
        prompt = prompt[index:]

        player = Player(bot=self.bot, ctx=self.ctx, prompt=prompt)
        await player.stream()

    def spotify(self, prompt):
        print("spotify")

    def cats(self):
        print("cat")

    async def anime(self, prompt, ctx):
        print("weeb")

        categories = ["Attack", "Bite", "Bloodsuck", "Blush", "Bonk", "Brofist",
                      "Cry", "Cuddle", "Dance", "Disgust", "Facedesk", "Facepalm",
                      "Flick", "Flirt", "Handhold", "Happy", "Harass", "Highfive", "Hug",
                      "Icecream", "Insult", "Kill", "Kiss"]
        randomCategoryIndex = random.randint(0, len(categories) - 1)
        category = categories[randomCategoryIndex]
        gifs = animegifs.Animegifs(category.lower())
        print(category)
        gif = gifs.get_gif()
        await ctx.channel.send(gif)
