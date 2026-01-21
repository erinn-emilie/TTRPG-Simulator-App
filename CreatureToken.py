class CreatureToken():
    def __init__(self, key=-1, name="", health=0.0, bio="""""", notes="""""", assets=[]):
        self.key = key
        self.name = name
        self.health = health
        self.bio = bio
        self.notes = notes
        self.assets = assets

    def getName(self) -> str:
        return self.name

    def getKey(self) -> int:
        return self.key
