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
        self.commandHeaderPath = os.path.join(self.worldPath, "datapacks", self.dataPackName, "data", self.dataPackName, "functions")
        self.commandPath = os.path.join(self.commandHeaderPath, self.dataPackName + "_sub_commands")

        self._generate_datapack_files()
        print(f"filesystem prepared: {self.commandHeaderPath}")

        # each list[x] should have commandsPerFile elements
        self.commands:list[list[str]] = [[]]
    def show_commands(self)->None:
        for over_command in self.commands:
            for command in over_command:
                print(f"{command}")
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
        Path(self.commandPath).mkdir(parents=True, exist_ok=True)
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
    def set_block(self, pos:tuple[int,int,int], block:str)->None:
        """set_block {pos[0]} {pos[1]} {pos[2]} minecraft:{block}"""
        command = f"setblock {pos[0]} {pos[1]} {pos[2]} minecraft:{block}"
        self._add_command(command)

    def fill(self, pos1:tuple[int,int,int], pos2:tuple[int,int,int], block:str):
        command = f"fill {pos1[0]} {pos1[1]} {pos1[2]} {pos2[0]} {pos2[1]} {pos2[2]} minecraft:{block}"
        self._add_command(command)

    def sphere(self, m:tuple[int,int,int], r:int, block:str):
        def is_inside(_x:int, _y:int, _z:int)->bool:
            if _x**2 + _y**2 + _z**2 < r**2:
                return True
            return False
        for dx in range(-r,r+1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    pos = m[0]+dx, m[2]+dy, m[1]+dz
                    if is_inside(*pos):
                        self.set_block(pos, block)
    # save
    def save(self)->None:
        # create sub_commands
        for i, commands in enumerate(self.commands):
            data = "\n".join(commands)
            name = os.path.join(self.commandPath, f"{self.dataPackName}_{i}.mcfunction")

            with open(name, "w") as f:
                f.write(data)

        # create the main .mcfunction file
        data = "\n".join([
            f"function {self.dataPackName}:{self.dataPackName}_sub_commands/{self.dataPackName}_{i}"
            for i in range(len(self.commands))])
        name = os.path.join(self.commandHeaderPath, f"{self.dataPackName}.mcfunction")
        with open(name, "w") as f:
            f.write(data)

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
    d.sphere((0,0,0), 3, "stone")
    d.show_commands()
