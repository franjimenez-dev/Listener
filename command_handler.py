import os
import random

import nextcord
import requests
import hashlib

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

        # Checks command needed from a given prompt-input

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
                cats_case = prompt.find("cats")
                if cats_case >= 0:
                    await self.cats(ctx)
                    return True
                else:
                    anime_case = prompt.find("anime")
                    if anime_case >= 0:
                        await self.anime(ctx)
                        return True
                    else:
                        persona_case = prompt.find("persona")
                        if persona_case >= 0:
                            await self.persona(ctx)
                            return True
                        else:

                            print("nothing")
                            return False
        else:
            print("nothing")
            return False

    async def youtube(self, prompt):

        # Search a vid on YouTube from an input given and plays it on voice channel

        index = prompt.find("youtube")
        index += len("youtube") + 1
        prompt = prompt[index:]

        player = Player(bot=self.bot, ctx=self.ctx, prompt=prompt)
        await player.stream()

    async def cats(self,ctx):

        # Displays a random cat image

        cat_response = requests.get("https://api.thecatapi.com/v1/images/search?")
        cat = cat_response.json()
        await ctx.channel.send(cat[0]['url'])

    async def anime(self, ctx):

        # Displays an anime picture of a random category

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

    async def persona(self, ctx):

        # Displays a picture of a person that doest not exists

        picture = requests.get("https://thispersondoesnotexist.com/image",
                         headers={'User-Agent': 'My User Agent 1.0'}).content

        h = hashlib.new("md5")
        h.update(picture)

        file = h.hexdigest() + ".jpeg"
        with open(file, "wb") as f:
            f.write(picture)

        myfile = nextcord.File(f"./{file}")
        await ctx.send(file=myfile)
        os.remove(f"./{file}")

