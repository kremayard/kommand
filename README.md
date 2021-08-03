<div align="center">
<h1>Kommand</h1>
<p>Simple command framework for Krema.</p>
<p><i>This project is a part of Krema.</i></p>
<br>
</div>

## Documentation
Check https://kremayard.github.io/kommand/
## Installation
Run `unikorn add kremayard kommand` and you are ready to go!

## Example
```py
from unikorn import kommand, krema

client = krema.Client(intents=0x7fff)
commands = Kommand(prefix=".") # Prefix for commands.

@commands.add(name="hello") # Add a new command.
async def hellofn(msg):
    if msg.author.bot: return

    await msg.reply(
        content="Hello Commands!" # Reply to message.
    )

commands.prepare(client) # Prepare all commands before start bot.
client.start("token", bot=True)
```