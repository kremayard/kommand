from dataclasses import dataclass
from typing import Callable


@dataclass
class Kommand:
    """Base class for Kommand.

    Args:
        prefix (str): Prefixes for commands.
    """

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.__commands: list = []

    def add(self, name: str = None, guild_only: bool = True, **kwargs):
        """Add new command decorator.

        Args:
            name (str, optional): Command name. (if None, it will get the function name as command name.)
            guild_only (bool, optional): if True, the command only will run if called on a guild. (default True.)
            **kwargs: Other informations if you want to add, You can get a command with these informations.
        """

        def decorator(fn: Callable):
            def wrapper():
                fn_name = name or fn.__name__

                kwargs["name"] = fn_name
                kwargs["guild_only"] = guild_only

                self.__commands.append(
                    (kwargs, fn)
                )

                return self.__commands

            return wrapper()

        return decorator

    def get(self, fn: Callable):
        """Get a command with command metadatas.

        Args:
            fn (Callable): a function that containes one parameter (metadata). This function must return a bool.

        Returns:
            tuple: A tuple that contains bot metadata and command function.
        """

        for command in self.__commands:
            if fn(command[0]) == True:
                return command

        return (None, None)

    def prepare(self, client):
        """Prepare commands for Krema client.

        Args:
            client (krema.models.Client): Client.
        """

        async def wrapper(message):
            content_splitted = message.content.strip()[
                len(self.prefix):].split(" ")

            if len(content_splitted) == 0:
                return

            command_name = content_splitted[0]
            metadata, command = self.get(
                lambda m: m.get("name") == command_name)

            if command is None:
                return
            if message.guild_id is None and metadata["guild_only"]:
                return

            await command(message)
            return

        client.events.append(
            ("message_create", wrapper)
        )
