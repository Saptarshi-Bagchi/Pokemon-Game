import random

weakness = {
    "Water": {
        "Fire": 2,
        "Water": 0.5,
        "Grass": 0.5,
        "Electric": 1
    },
    "Electric": {
        "Fire": 1,
        "Water": 2,
        "Grass": 0.5,
        "Electric": 0.5
    },
    "Fire": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Electric": 1
    },
    "Grass": {
        "Fire": 0.5,
        "Water": 2,
        "Grass": 0.5,
        "Electric": 1
    }
}

def attempt_hit(attacker, defender, damage_amount):
    if defender.shield:
        print(f"{defender.name} is protected!")
        defender.shield = False
        defender.last_protect = True
        return False
    defender.take_damage(attacker, damage_amount)
    return True

class Pokemon:
    def __init__(self, name, pokemon_type, speed, hp):
        self.name = name
        self.pokemon_type = pokemon_type
        self.speed = speed
        self.__max_hp = hp
        self.hp = self.__max_hp
        self.reason = "none"
        self.shield = False
        self.last_protect = False

    def display(self):
        print(f"Name: {self.name}")
        print(f"Type: {self.pokemon_type}")
        print(f"Speed: {self.speed}")
        print(f"Health: {self.hp}")

    def attack(self):
        if self.reason == "none":
            print(f"{self.name} is attacking!")
            return True
        if self.reason == "paralyze":
            if random.random() < 0.5:
                print(f"{self.name} is paralyzed and cannot move!")
                return False
            else:
                print(f"{self.name} fights through paralysis!")
                return True
        print(f"{self.name} is affected with {self.reason}, they cannot attack!")
        return False

    def protect(self):
        if self.last_protect:
            print(f"{self.name} tried to Protect again, but it failed!")
            self.last_protect = False
            return
        print(f"{self.name} is protecting!")
        self.shield = True
        self.last_protect = True

    def heal(self, heal_amount):
        if self.hp + heal_amount > self.__max_hp:
            self.hp = self.__max_hp
            print(f"{self.name} is fully healed!!")
        else:
            self.hp += heal_amount
            print(f"{self.name} healed for {heal_amount} hp!!")

    def take_damage(self, opponent, damage_amount):
        multiplier = weakness[opponent.pokemon_type][self.pokemon_type]
        real_damage = damage_amount * multiplier
        if multiplier == 0.5:
            print("The attack is not very effective!")
        elif multiplier == 2:
            print("The attack was very effective!")
        if self.hp - real_damage <= 0:
            self.hp = 0
            print(f"{self.name} took {int(real_damage)} dmg, {self.name} has fainted!!")
        else:
            self.hp -= real_damage
            print(f"{self.name} took {int(real_damage)} dmg, it has {int(self.hp)} HP left!")

    def recoil(self, damage_amount):
        if self.hp - damage_amount <= 0:
            self.hp = 0
            print(f"{self.name} took {damage_amount} recoil dmg, {self.name} has fainted!!")
        else:
            self.hp -= damage_amount
            print(f"{self.name} took {damage_amount} recoil dmg, it has {self.hp} HP left!")

class FirePokemon(Pokemon):
    moves = ["FireBall", "FlameThrower", "HeatCrash", "Protect"]

    def __init__(self, name, speed, hp):
        super().__init__(name, "Fire", speed, hp)

    def do_move(self, move, opponent):
        if self.reason != "none" and random.random() < 0.5:
            print(f"{self.name} recovered from {self.reason}!")
            self.reason = "none"
        if move != "Protect":
            self.last_protect = False
        match move:
            case "FireBall":
                self.fireball(opponent)
            case "FlameThrower":
                self.flamethrower(opponent)
            case "HeatCrash":
                self.heatcrash(opponent)
            case "Protect":
                self.protect()

    def fireball(self, opponent):
        if super().attack():
            print(f"{self.name} used Fire Gun!")
            attempt_hit(self, opponent, random.randint(20, 25))

    def flamethrower(self, opponent):
        if super().attack():
            print(f"{self.name} used Flame Thrower!")
            if attempt_hit(self, opponent, random.randint(8, 15)) and opponent.hp != 0:
                attempt_hit(self, opponent, random.randint(8, 15))

    def heatcrash(self, opponent):
        if super().attack():
            print(f"{self.name} used Heat Crash!")
            if attempt_hit(self, opponent, random.randint(10, 35)):
                self.recoil(random.randint(5, 15))

class ElectricPokemon(Pokemon):
    moves = ["ThunderBolt", "ElectroBall", "Discharge", "Protect"]

    def __init__(self, name, speed, hp):
        super().__init__(name, "Electric", speed, hp)

    def do_move(self, move, opponent):
        if self.reason != "none" and random.random() < 0.5:
            print(f"{self.name} recovered from {self.reason}!")
            self.reason = "none"
        if move != "Protect":
            self.last_protect = False
        match move:
            case "ThunderBolt":
                self.thunderbolt(opponent)
            case "ElectroBall":
                self.electroball(opponent)
            case "Discharge":
                self.discharge(opponent)
            case "Protect":
                self.protect()

    def thunderbolt(self, opponent):
        if super().attack():
            print(f"{self.name} used Thunder Bolt!")
            if attempt_hit(self, opponent, random.randint(12, 20)):
                if random.random() < 0.4:
                    opponent.reason = "paralyze"
                    print(f"{opponent.name} got paralyzed!")

    def electroball(self, opponent):
        if super().attack():
            print(f"{self.name} used Electro Ball!")
            if attempt_hit(self, opponent, random.randint(14, 24)):
                if random.random() < 0.2:
                    opponent.reason = "paralyze"
                    print(f"{opponent.name} got paralyzed!")

    def discharge(self, opponent):
        if super().attack():
            print(f"{self.name} used Discharge!")
            if attempt_hit(self, opponent, random.randint(10, 30)):
                self.recoil(random.randint(5, 10))

class WaterPokemon(Pokemon):
    moves = ["WaterGun", "AquaJet", "Recover", "Protect"]

    def __init__(self, name, speed, hp):
        super().__init__(name, "Water", speed, hp)

    def do_move(self, move, opponent):
        if self.reason != "none" and random.random() < 0.5:
            print(f"{self.name} recovered from {self.reason}!")
            self.reason = "none"
        if move != "Protect":
            self.last_protect = False
        match move:
            case "WaterGun":
                self.watergun(opponent)
            case "AquaJet":
                self.aquajet(opponent)
            case "Recover":
                print(f"{self.name} used Recover!")
                self.heal(random.randint(22, 26))
            case "Protect":
                self.protect()

    def watergun(self, opponent):
        if super().attack():
            print(f"{self.name} used Water Gun!")
            attempt_hit(self, opponent, random.randint(18, 24))

    def aquajet(self, opponent):
        if super().attack():
            print(f"{self.name} used Aqua Jet!")
            attempt_hit(self, opponent, random.randint(16, 26))

class GrassPokemon(Pokemon):
    moves = ["RazorVine", "VineWhip", "LeechSeed", "Protect"]

    def __init__(self, name, speed, hp):
        super().__init__(name, "Grass", speed, hp)

    def do_move(self, move, opponent):
        if self.reason != "none" and random.random() < 0.5:
            print(f"{self.name} recovered from {self.reason}!")
            self.reason = "none"
        if move != "Protect":
            self.last_protect = False
        match move:
            case "RazorVine":
                self.razorvine(opponent)
            case "VineWhip":
                self.vinewhip(opponent)
            case "LeechSeed":
                self.leechseed(opponent)
            case "Protect":
                self.protect()

    def razorvine(self, opponent):
        if super().attack():
            print(f"{self.name} used Razor Vine!")
            if attempt_hit(self, opponent, random.randint(6, 12)) and opponent.hp != 0:
                if attempt_hit(self, opponent, random.randint(6, 12)) and opponent.hp != 0:
                    attempt_hit(self, opponent, random.randint(6, 12))

    def vinewhip(self, opponent):
        if super().attack():
            print(f"{self.name} used Vine Whip!")
            if attempt_hit(self, opponent, random.randint(8, 15)) and opponent.hp != 0:
                attempt_hit(self, opponent, random.randint(8, 15))

    def leechseed(self, opponent):
        if super().attack():
            print(f"{self.name} used Leech Seed!")
            if attempt_hit(self, opponent, random.randint(15, 20)):
                self.heal(random.randint(6, 12))

pikachu = ElectricPokemon("Pikachu", 107, 90)
charmander = FirePokemon("Charmander", 105, 100)
squirtle = WaterPokemon("Squirtle", 103, 120)
bulbasaur = GrassPokemon("Bulbasaur", 106, 110)

pokemons = [pikachu, charmander, squirtle, bulbasaur]

while True:
    print("Choose a pokemon!")
    print("1. Pikachu")
    print("2. Charmander")
    print("3. Squirtle")
    print("4. Bulbasaur")
    try:
        choice = int(input("Enter your choice (1-4): "))
        if choice not in [1, 2, 3, 4]:
            print("Incorrect choice! Please select 1, 2, 3, or 4.")
        else:
            break
    except ValueError:
        print("Invalid input! Please enter a number between 1 and 4.")

team = pokemons[choice - 1]
print(f"\nYou chose {team.name}!\n")
team.display()
print()
opp = random.choice([p for p in pokemons if p != team])
print(f"A wild {opp.name} appears!")
print("Battle Begins!\n")

def take_turn(current, other, is_player):
    if current.hp == 0 or other.hp == 0:
        return
    if is_player:
        print("Available moves:", "  ".join(current.moves))
        while True:
            move = input("Enter your move: ")
            if move not in current.moves:
                print("Incorrect Move! Try again.")
            else:
                print(f"You chose {move}!\n")
                break
    else:
        move = random.choice(current.moves)
    current.do_move(move, other)
    print()

while team.hp > 0 and opp.hp > 0:
    if team.speed > opp.speed:
        order = [(team, opp, True), (opp, team, False)]
    elif team.speed < opp.speed:
        order = [(opp, team, False), (team, opp, True)]
    else:
        if random.random() < 0.5:
            order = [(team, opp, True), (opp, team, False)]
        else:
            order = [(opp, team, False), (team, opp, True)]

    for actor, target, is_player in order:
        take_turn(actor, target, is_player)
        if target.hp == 0:
            break

    if team.shield:
        team.shield = False
    if opp.shield:
        opp.shield = False