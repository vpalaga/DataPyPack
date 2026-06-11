import tomllib  # Python 3.11+
from typing import Any
import os
from pathlib import Path
import json
from src.pack_format import get_pack_format

class DataPyPypack:
    version:str = "1.0.0"
    def __init__(self, configPath:str=r"config.toml")->None:
        # user inputs -----------------------
        self.configPath = configPath
        self.config = self._load_config()

        self.minecraftFolder:str =      self.config["output"]["minecraft_folder"]
        self.worldName:str =            self.config["output"]["world_name"]
        self.minecraftVersion:str =     self.config["output"]["minecraft_version"]

        self.commandsPerFile:int =      self.config["datapack"]["commands_p_file"]
        self.dataPackName:str =         self.config["datapack"]["datapack_name"]
        self.datapackVersion:str =      self.config["datapack"]["datapack_version"]
        self.datapackDescription:str =  self.config["datapack"]["datapack_description"]
        self._check_user_inputs()

        # internal data section -----------------------
        # world path
        self.worldPath = os.path.join(self.minecraftFolder, "saves", self.worldName)
        self.commandPath = os.path.join(self.worldPath, "datapacks", self.dataPackName, "data", self.dataPackName, "functions")
        self._generate_datapack_files()
        print(f"filesystem prepared: {self.commandPath}")

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
        if not os.path.exists(self.minecraftFolder):
            raise IsADirectoryError(self.minecraftFolder)
        # check command num has to be smaller than 5000
        if not 0 < self.commandsPerFile < 5000:
            raise ValueError(f"max commands: not 0<n<5000 : {self.commandsPerFile}")
        #check minecraft version
    def _generate_datapack_files(self)->None:
        # Create a new folder inside an existing one
        Path(os.path.join(self.commandPath, self.dataPackName + "_sub_commands")).mkdir(parents=True, exist_ok=True)
        # create .mcmeta header file
        headerPath = os.path.join(self.worldPath, "datapacks", self.dataPackName, "pack.mcmeta")
        pack_format = get_pack_format(self.minecraftVersion, "data")
        data = {
            "pack": {
                "pack_format": pack_format,
                "description": self.datapackDescription + self.datapackVersion
            }
        }
        with open(headerPath, "w") as f:
            json.dump(data, f, indent=2)


    @staticmethod
    def _check_command_validity(command:str)->bool:
        is_valid = True
        if not is_valid:
            raise DataPyPypack.Errors.InvalidCommandError(command)
        return True # for now

    def _add_command(self, command:str)->None:

        if len(self.commands[-1]) >= self.commandsPerFile:
            # check if commands are not full:
            if len(self.commands) == 5000:
                raise DataPyPypack.Errors.HeaderCommandFileTooLarge(None)

            # add new command list
            self.commands.append([])

        self.commands[-1].append(command)

    # commands
    def command(self, command:str)->None:
        self._add_command(command)
    def set_block(self, pos:tuple[int,int,int], block:str):
        """set_block {pos[0]} {pos[1]} {pos[2]} minecraft:{block}"""
        command = f"set_block {pos[0]} {pos[1]} {pos[2]} minecraft:{block}"
        self._add_command(command)

    def save(self)->None:
        pass

    class Errors:
        class InvalidCommandError(Exception):
            def __init__(self, message):
                self.message = message
                super().__init__("invalid command: '" + self.message + "'")

        class HeaderCommandFileTooLarge(Exception):
            def __init__(self, message):
                self.message = message
                super().__init__("too many header commands: '" + self.message + "'")

if __name__ == "__main__":
    d = DataPyPypack()