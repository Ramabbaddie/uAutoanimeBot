import asyncio
from pyrogram import filters
from pyrogram.types import Message

from contextlib import closing, suppress
from pyrogram import idle
import AutoAnimeBot.modules.vote
from AutoAnimeBot import app
from AutoAnimeBot.web_support import start_web_server

loop = asyncio.get_event_loop()


@app.on_message(filters.command(["start", "help", "ping"]))
async def start(bot, message: Message):
    await message.reply_photo(
        "assets/thumb.jpg",
        caption="⭐️ **Bot Is Online...**\n\n**Updates :** @YourChannel **| Support :** @YourSupportGroup",
    )


@app.on_message(filters.command("logs"))
async def logs(bot, message: Message):
    await message.reply_document(
        "logs.txt",
        caption="AutoAnimeBot Logs, Send this to your admin if you need help",
    )


async def main():
    # Start web server for Render Free Tier
    await start_web_server()
    
    await app.start()

    await idle()
    app.logger.info("BOT STOPPED")
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()


if __name__ == "__main__":
    # install()  <-- Removed uvloop to prevent asyncio conflicts on HF
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(main())
            loop.run_until_complete(asyncio.sleep(3.0))
