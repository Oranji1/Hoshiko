# Hoshiko

**Hoshiko** is a Discord bot focused on anime and manga search and information retrieval.  
It connects to multiple APIs such as AniList and MyAnimeList through an asynchronous and modular architecture.

> [!WARNING]
> Although the current project version is `v0.1.0`, Hoshiko should be considered **an early alpha**.  
> Expect unoptimized code, missing features, ugly-written code, and inconsistent design decisions that may change significantly in future versions.



## Features

- Search for anime and manga from multiple sources (AniList, MAL, etc.)
- That's... pretty much it for now... (Hey, I told you it was an alpha.)



## Setup


#### Prerequisites:

Hoshiko uses **[uv](https://docs.astral.sh/uv/)** for dependency management. First, make sure you have it [installed](https://docs.astral.sh/uv/getting-started/installation/).


#### Installation

1. Clone the repository and install dependencies:
   ```sh
   git clone https://github.com/Oranji1/Hoshiko.git
   cd Hoshiko
   uv sync
   ```

2. Create a config file named `config.json` (or rename the provided `example.config.json`) with your bot token:
   ```json
   {
       "bot": {
           "token": "YOUR_BOT_TOKEN_HERE"
       }
   }
   ```
3. To run the bot simply run:
   ```sh
   uv run main.py
   ```

> [!NOTE]
> Hoshiko uses uvloop automatically if it is installed.
> If not, it will fall back to Python's built-in asyncio's event loop without any configuration required.  
> This means that if you don't like fast things, you can just uninstall it.



## Planned improvements

- Use slash commands instead of traditional prefix commands.
- Proper command help and descriptions.
- Better API coverage and beyond AniList and MAL.
- Implement an API fallback system and improve API error handling.
- Replace `pydantic` with `msgspec` and improve model structure.
- Replace `cachetools` with a custom persistent async cache implementation.
- Cleaner logging and exception tracing.
- General code quality, design, and performance improvements (y'know, fixing the "ugly-written code" I warned you about.)
- And a bunch of other things that I can't add here, cuz otherwise the list would be too long...