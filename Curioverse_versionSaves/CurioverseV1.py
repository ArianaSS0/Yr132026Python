print ("\033[1;36;40m Program running \033[0m") #Cyan text


# --- CREATING LIBRARYS ---  (Gamification element)
class UAStats: #User affected ststs
    def __init__(self):
        self.activity = 0 #affected if ticked for done today
        self.attention = 0 #affected if notes taken
        self.growthlvl = 1
        self.affection = (self.activity + self.attention + (self.growthlvl/self.growthlvl))/3 #overall

class GAStats: #Game affected stats
    def __init__(self):
        self.social = 0
        self.curiosity = 0.5
        self.fun = 0.5
        self.confidence = (self.social + self.fun + (1- self.curiosity))/3
        self.mood = (self.social + self.curiosity + self.fun + self.confidence)/4

class TWAStats: #Time/Weather affected stats
    def __init__(self):
        self.sleep = 1
        self.hunger = 1
        self.tempurature = 0
        self.dampness = 0
        self.health = (self.sleep + self.hunger + (1- self.tempurature) + (1- self.dampness))/4

class Pet: #allows calling of other clasess through Pet
    def __init__(self):
        self.ua = UAStats()
        self.ga = GAStats()
        self.twa = TWAStats()
pet = Pet()

# --- Notes ---

# Create new curio (name,category)
# Forms, Data storage, Image upload
# Edit records (add/remove)
# Time tracking
# Ability to choose a curio, then it tell you stats, details, and it allows you to enter new entrys
# Ability to move to Main world, Graveyard and museim, which changes what is accessable
# ability to see overall ststistics
# some point create the ability to search and filter

#Once begining to work on GUI, each action or process should be displayed in the output box

# --- PLAYTHROUGH ---

print("Affection = ",f"{pet.ua.affection:.2f}") #.2f means to 2dp
print("Confidence = ",f"{pet.ga.confidence:.2f}") 
print("Mood = ",f"{pet.ga.mood:.2f}")
print("Health = ",f"{pet.twa.health:.2f}")


print ("\033[1;31;40m Program closing \033[0m") #Red text