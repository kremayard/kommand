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
                    (fn_name, guild_only, kwargs, fn)
                )

                return self.__commands

            return wrapper()

        return decorator

    def get(self, fn: Callable):
        """Get a command with command metadatas.
        
        Args:
            fn (Callable): a function that containes one parameter (metadata). This function must return a bool.

        Returns:
            dict: All informations for command that includes name, guild_only and other metadatas.
        """

        for command in self.__commands:
            if fn(command[2]) == True:
                return command[2]