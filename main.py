import os
from dotenv import load_dotenv
import time

global vc
global contexto

load_dotenv()

TOKEN = os.getenv('TOKEN')

import nextcord
import nextcord.ext.commands as commands
import nextcord.ext.voicerecording as voicerecording
import whisper

model = whisper.load_model("small")
bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=nextcord.Intents.all())
bot.connections = {}

from command_handler import CommandHandler

_commandHandler = CommandHandler(bot)


async def whisper_command_handler(prompt):
    return await _commandHandler.check_command(prompt, contexto)


async def get_vc(message: nextcord.Message):
    original_vc = message.author.voice
    if not original_vc:
        await message.channel.send("You're not in a vc right now")
        return
    connection = bot.connections.get(message.guild.id)
    if connection:
        if connection.channel.id == message.author.voice.channel.id:
            return connection

        await connection.move_to(original_vc.channel)
        return connection
    else:
        original_vc = await original_vc.channel.connect()
        bot.connections.update({message.guild.id: original_vc})
        return original_vc


async def finished_callback(sink: voicerecording.FileSink, channel, *args):
    stopListening = False
    for f in sink.get_files():
        result = model.transcribe(f, fp16=False)
        stopListening = await whisper_command_handler(result['text'])

    sink.destroy()
    if not stopListening:
        await recording(contexto, 0, 1000000)


@bot.command(name="join")
async def join(ctx: commands.Context, itime: int = 0, size: int = 1000000):
    global contexto
    contexto = ctx
    global vc
    vc = await get_vc(ctx.message)

    await recording(contexto, itime, size)


@bot.command(name="resume")
async def resume(ctx: commands.Context):
    await recording(ctx, 0, 1000000)


async def recording(ctx: commands.Context, itime: int = 0, size: int = 1000000):
    print("started")
    await vc.start_listening(
        voicerecording.FileSink(encoding=voicerecording.wav_encoder, filters={'time': itime, 'max_size': size}),
        finished_callback, [ctx.channel])

    time.sleep(12)
    print("stopped")
    await vc.stop_listening()


@bot.listen
async def on_voice_state_update(self, member, before, after):
    if member.id != self.user.id:
        return
    # Filter out updates other than when we leave a channel we're connected to
    if member.guild.id not in self.connections or (not before.channel and after.channel) or (
            before.channel == after.channel):
        return
    del self.connections[member.guild.id]
    print("Disconnected")


if __name__ == '__main__':
    voicerecording.cleanuptempdir()
    bot.run(TOKEN)
