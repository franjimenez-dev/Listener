import asyncio
import nextcord
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Player:
    def __init__(self, *, bot, ctx, prompt):
        self.bot = bot
        self.ctx = ctx
        self.prompt = prompt

    async def stream(self):

        # Plays music on a voice channel

        data = ytdl.extract_info(f"ytsearch:{self.prompt}", download=False)
        if 'entries' in data:
            data = data['entries'][0]

        async with self.ctx.typing():
            player = await YTDLSource.from_url(data["webpage_url"], loop=self.bot.loop, stream=True)
            self.ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await self.ctx.send(f'**Now playing:** {player.title}')


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        # Returns youtube video data from an url

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
