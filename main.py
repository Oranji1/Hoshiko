from bot.hoshiko import Hoshiko
try:
    import uvloop
except ModuleNotFoundError:
    import asyncio
    RUNTIME = asyncio.run
else:
    RUNTIME = uvloop.run

async def main():
    async with Hoshiko() as bot:
        await bot.start()

if __name__ == "__main__":
    RUNTIME(main())