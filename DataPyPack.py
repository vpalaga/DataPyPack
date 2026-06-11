import tomllib  # Python 3.11+
from typing import Any
import os

class DataPyPypack:
    version:str = "1.0.0"
    def __init__(self, configPath:str=r"config.toml")->None:
        # user inputs -----------------------
        self.configPath = configPath
        self.config = self._load_config()

        self.minecraftWorldsPath:str =  self.config["output"]["minecraft_worlds_folder"]
        self.commandsPerFile:int =      self.config["output"]["commands_p_file"]
        self.minecraftVersion:str =     self.config["output"]["minecraft_version"]
        self.dataPackName:str =         self.config["output"]["datapack_name"]
        self.datapackVersion:str =      self.config["output"]["datapack_version"]

        self._check_user_inputs()

        # internal data section -----------------------

        # each list[x] should have commandsPerFile elements
        self.commands:list[list[str]] = [[]]

    def _load_config(self)->dict[str,Any]:
        try:
            with open(self.configPath, "rb") as f:
                config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            print(f"Config file error: {e}")
            exit(1)
        return config
    def _check_user_inputs(self)->None:
        # check world path
        if not os.path.exists(self.minecraftWorldsPath):
            raise IsADirectoryError(self.minecraftWorldsPath)
        # check command num has to be smaller than 5000
        if not 0 < self.commandsPerFile < 5000:
            raise ValueError(f"max commands: not 0<n<5000 : {self.commandsPerFile}")
        #check minecraft version

    @staticmethod
    def _check_command_validity(command:str)->bool:
        is_valid = True
        if not is_valid:
            raise DataPyPypack.Errors.InvalidCommandError(command)
        return True # for now

    def _add_command(self, command:str)->None:

        if len(self.commands[-1]) >= self.commandsPerFile:
            # add new command list
            self.commands.append([])

        self.commands[-1].append(command)

    # commands
    def command(self, command:str)->None:
        self._add_command(command)

    # write to files
    def save(self)->None:
        pass

    class Errors:
        class InvalidCommandError(Exception):
            def __init__(self, message):
                self.message = message
                super().__init__("invalid command: '" + self.message + "'")

if __name__ == "__main__":
    d = DataPyPypack()