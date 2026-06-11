#   DataPyPack
> python module that makes creating Minecraft datapacks easy 

 --- 

goal: it makes creating minecraft command chains less PITA

## usage:
+ set your stuff up in  `config.toml`  
+ and use `DataPyPack.py` to gen the folders and command files

````python
# example usage:
from DataPyPack import DataPyPypack

pack = DataPyPypack()

# add your commands
pack.set_block((0,0,0), "dirt")
pack.command("say hello")

# save as minecraft datapack
pack.save()
````

you can add your own methods to DataPyPack (please merge with this) 
just by adding your method into the DataPyPack class by using self._add_command(): 

````python
    ...
    # commands
    def command(self, command:str)->None:
        ...
    def set_block(self, pos:tuple[int,int,int], block:str)->None:
        ...
    
    def my_method(self, ...)->None:
        #do something 
        
        self._add_command("some command")
    ...
````

## please fix:
+ minecraft versions after 1.20 will not deal with the functions correctly I don't know why, and I have spent too much time trying...

## for future
+ focus on other functionalities of minecraft datapacks 

### credits
+ *developed by VPalaga*
+ your name here... 