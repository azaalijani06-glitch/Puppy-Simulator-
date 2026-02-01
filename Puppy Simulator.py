import time
import random
import os
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ---------------- SAVE DIRECTORY ----------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(SCRIPT_DIR, "Puppy Simulator Saves")
os.makedirs(SAVE_DIR, exist_ok=True)

def Get_AmountSaves():
    return len([f for f in os.listdir(SAVE_DIR) if f.endswith(".json")])

# ---------------- DATA ----------------
DialogOptions = [
    "Thats cute!", "Ew!", "Wow thats a nice name!",
    "Couldnt have picked a better name!", "Interesting choice!",
    "Cool name!", "Hey there!", "Greetings!"
]

UsableItems = [
    {"Health Potion": {"HealAmount": 20}},
    {"Strength Elixir": {"BoostAmount": 10}},
    {"Damage Scroll": {"DamageAmount": 15}},
    {"Health Elixir": {"HealAmount": 50}},
    {"Mega Damage Scroll": {"DamageAmount": 30}},
    {"Ultra Strength Elixir": {"BoostAmount": 25}},
    {"Ultimate Health Potion": {"HealAmount": 100}},
    {"Elixir Of Life": {"HealAmount": 200}}
]

loot_table = ["Health Potion", "Strength Elixir", "Damage Scroll", "Nothing"]

# ---------------- CLASSES ----------------
class Animal:
    def __init__(self, species, name, health=100):
        self.species = species
        self.name = name
        self.health = health

    def TakeDamage(self, damage):
        self.health -= damage
        print(Fore.RED + f"{self.name} the {self.species} took {damage} damage!")

    def Attack(self, target):
        dmg = random.randint(5, 20)
        print(f"{self.name} attacks {target.name}...", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.2)
        print(f" HIT!")
        target.TakeDamage(dmg)

class Dog:
    def __init__(self, name, species, health, CurrentBattle=None, CurrentOpponent=None, Inventory=None):
        self.name = name
        self.species = species
        self.health = health
        self.CurrentBattle = CurrentBattle
        self.CurrentOpponent = CurrentOpponent
        self.Inventory = Inventory if Inventory else []
        self.DamageRange = (10, 30)

    def Bark(self):
        print(Fore.CYAN + "Woof! 🐶")

    def Fetch(self, item):
        print(Fore.MAGENTA + f"{self.name} fetched the {item}!")

    def TakeDamage(self, dmg):
        self.health -= dmg
        print(Fore.RED + f"{self.name} took {dmg} damage!")

    def Attack(self, target):
        crit = random.randint(1, 100) <= 20
        dmg = random.randint(self.DamageRange[0], self.DamageRange[1])
        if crit:
            dmg *= 2
            print(Fore.YELLOW + "Critical hit!")
        print(f"{self.name} attacks {target.name}...", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.2)
        print(f" HIT!")
        target.TakeDamage(dmg)

    def Battle(self, opponent):
        print(Fore.GREEN + f"{self.name} is battling {opponent.name}!")
        self.CurrentBattle = opponent.name
        self.CurrentOpponent = opponent

        while self.health > 0 and opponent.health > 0:
            self.Attack(opponent)
            if opponent.health <= 0:
                print(Fore.GREEN + f"{opponent.name} has been defeated!")
                self.CurrentBattle = None
                self.CurrentOpponent = None
                # Random loot drop
                drop = random.choice(loot_table)
                if drop != "Nothing":
                    print(Fore.MAGENTA + f"You found a {drop}!")
                    self.Inventory.append(drop)
                return

            time.sleep(1)
            opponent.Attack(self)

            if self.health <= 0:
                print(Fore.RED + f"{self.name} has been defeated!")
                self.CurrentBattle = None
                self.CurrentOpponent = None
                print("Better luck next time!")
                self.health = 100
                return

    def ShowWounds(self):
        bar = "#" * (self.health // 10)
        bar += " " * (10 - len(bar))
        print(f"{self.name}: [{bar}] {self.health} HP")

    def ShowInventory(self):
        if not self.Inventory:
            print(f"{self.name}'s inventory is empty.")
        else:
            print(f"{self.name}'s Inventory: " + ", ".join(self.Inventory))

    def UseItem(self, item):
        if item in self.Inventory:
            print(f"{self.name} used {item}!")
            GetItemAbility = next((i[item] for i in UsableItems if item in i), None)
            if GetItemAbility:
                if "HealAmount" in GetItemAbility:
                    self.health += GetItemAbility["HealAmount"]
                    print(Fore.GREEN + f"{self.name} healed for {GetItemAbility['HealAmount']} HP!")
                elif "BoostAmount" in GetItemAbility:
                    self.DamageRange = (self.DamageRange[0] + GetItemAbility["BoostAmount"], self.DamageRange[1] + GetItemAbility["BoostAmount"])
                    self.health += GetItemAbility["BoostAmount"]
                    print(Fore.YELLOW + f"{self.name} gained a {GetItemAbility['BoostAmount']} boost!")
                elif "DamageAmount" in GetItemAbility:
                    self.DamageRange = (self.DamageRange[0] + GetItemAbility["DamageAmount"], self.DamageRange[1] + GetItemAbility["DamageAmount"])
                    print(Fore.YELLOW + f"{self.name} deals {GetItemAbility['DamageAmount']} more damage!")
            self.Inventory.remove(item)
        else:
            print(f"{item} not found in inventory.")

# ---------------- LOAD/NEW GAME ----------------
LoadSave = input("Do you want to load a previous save? (yes/no): ").strip().lower()
SaveStatus = False  # True if loading existing save

if LoadSave == "yes" and Get_AmountSaves() > 0:
    print(f"You have {Get_AmountSaves()} saves.")
    SaveStatus = True
    SaveNumber = int(input("Choose save number: "))
    SavePath = os.path.join(SAVE_DIR, f"Save{SaveNumber}.json")
    with open(SavePath, "r") as f:
        data = json.load(f)
    s = data["Puppy Status"]
    MyPuppy = Dog(
        s["Name"],
        s["Species"],
        s["Health"],
        s.get("CurrentBattle"),
        None,
        s.get("Inventory", [])
    )
elif LoadSave == "no" or Get_AmountSaves() == 0:
    print("HI THERE... welcome to puppy simulator!")
    PuppyName = input("Pick your puppy name: ")
    print(f"So your puppy name is {PuppyName}? {random.choice(DialogOptions)}")
    MyPuppy = Dog(PuppyName, "Dog", 100)
    SaveStatus = False  # New game saves to new file

# ---------------- MAIN LOOP ----------------
while True:
    print(f"\nWhat do you want {MyPuppy.name} to do? (Bark/Fetch/Battle/Quit/Show Wounds/Show Inventory/Use Item)")
    choice = input().lower()
    
    if choice == "bark":
        MyPuppy.Bark()
    
    elif choice == "fetch":
        item = input("Fetch what? ")
        MyPuppy.Fetch(item)
    
    elif choice == "battle":
        species = input("Opponent species: ")
        name = input("Opponent name: ")
        enemy = Animal(species, name, 100)
        MyPuppy.Battle(enemy)
    
    elif choice == "quit":
        # Handle SaveStatus
        if SaveStatus:
            # Overwrite the current save
            SaveNum = Get_AmountSaves()
        else:
            # New save file
            SaveNum = Get_AmountSaves() + 1
        
        SavePath = os.path.join(SAVE_DIR, f"Save{SaveNum}.json")
        save_data = {
            "Puppy Status": {
                "Name": MyPuppy.name,
                "Species": MyPuppy.species,
                "Health": MyPuppy.health,
                "CurrentBattle": MyPuppy.CurrentBattle,
                "CurrentOpponent": (
                    {
                        "Name": MyPuppy.CurrentOpponent.name,
                        "Species": MyPuppy.CurrentOpponent.species,
                        "Health": MyPuppy.CurrentOpponent.health
                    } if MyPuppy.CurrentOpponent else None
                ),
                "Inventory": MyPuppy.Inventory
            }
        }
        with open(SavePath, "w") as f:
            json.dump(save_data, f, indent=4)
        
        print("Game saved. Goodbye!")
        break
    
    elif choice == "show wounds":
        MyPuppy.ShowWounds()
    
    elif choice == "show inventory":
        MyPuppy.ShowInventory()
    
    elif choice == "use item":
        item = input("Which item do you want to use? ")
        MyPuppy.UseItem(item)
    
    else:
        print("Invalid option.")