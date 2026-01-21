import json
from CreatureToken import CreatureToken


class Creatures():
    JSON_FILE_PATH = "Creatures.json"

    def __init__(self):
        self.dictOfCreatures = {}
        self.listOfCreatures = []
        try:
            with open(self.JSON_FILE_PATH, 'r') as file:
                self.dictOfCreatures = json.load(file)
                '''self.__setup()'''
        except FileNotFoundError:
            print("Couldn't find JSON file with creature tokens!")
        except json.JSONDecodeError:
            print("JSON file with creature tokens couldn't be decoded")

    def getListOfCreatures(self) -> list:
        return self.listOfCreatures

    def getCreatureByName(self, name:str) -> CreatureToken:
        for creature in self.listOfCreatures:
            if(name == creature.getName()):
                return creature
        return None

    def getCreatureByKey(self, key:int) -> CreatureToken:
        for creature in self.listOfCreatures:
            if(key == creature.getKey()):
                return creature
        return None

    '''
    def __setup(self):
        for creature in self.dictOfCreatures:
            key = creature["key"]
            name = creature["name"]
            health = creature["health"]
            bio = creature["bio"]
            notes = creature["notes"]
            assets = creature["assets"]

            creatureObj = CreatureToken(key, name, health, bio, notes, assets)
            self.listOfCreatures.append(creatureObj)'''








    
