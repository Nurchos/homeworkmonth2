from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.__stun = False

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        if not self.__stun:
            for hero in heroes:
                if hero.health > 0:
                    if type(hero) == Berserk and self.defence != hero.ability:
                        block = choice([5, 10])
                        hero.blocked_damage = block
                        hero.health -= (self.damage - block)
                    else:
                        hero.health -= self.damage
        else:
            print(f'Boss {self.name} is stunned and skips this round!')
            self.__stun = False

    def __str__(self):
        return f'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRIT')

    def apply_super_power(self, boss, heroes):
        coef = randint(2, 5)
        boss.health -= self.damage * coef
        print(f'Warrior {self.name} hit critically {self.damage * coef}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')
        self.rounds_boost_used = 0

    def apply_super_power(self, boss: Boss, heroes: list):
        global round_number
        if self.rounds_boost_used < 4 and self.health > 0:
            attack_boost = randint(1, 5)
            for hero in heroes:
                if hero.health > 0 and not isinstance(hero, Witcher) and not isinstance(hero, King):
                    hero.damage += attack_boost
            self.rounds_boost_used += 1
            print(f'Magic boosted the attack of all heroes by {attack_boost} in round {round_number}')
        elif self.rounds_boost_used >= 4:
            print(f'Magic boost is no longer available in round {round_number}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} damage to boss')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')
        self.__used_power = False

    def apply_super_power(self, boss, heroes):
        if not self.__used_power:
            for hero in heroes:
                if hero.health == 0:
                    print(f'{self.name} жертвует собой, чтобы возродить {hero.name}')
                    hero.health = self.health
                    self.health = 0
                    self.__used_power = True
                    break


class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STEAL')
        self.__stolen_health = 0
        self.__rounds_since_last_steal = 0

    def apply_super_power(self, boss: Boss, heroes: list):
        global round_number
        if self.__rounds_since_last_steal == 1:
            if boss.health > 0 and self.health > 0:
                stolen_health = randint(10, 30)
                self.__stolen_health = stolen_health
                boss.health -= stolen_health
                hero = choice([hero for hero in heroes if hero.health > 0])
                hero.health += stolen_health
                print(f'Hacker {self.name} stole {stolen_health} health from the Boss and gave it to {hero.name} in round {round_number}')
            self.__rounds_since_last_steal = 0
        else:
            self.__rounds_since_last_steal += 1

    @property
    def stolen_health(self):
        return self.__stolen_health


class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'SuperAbility.CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        global round_number
        if round_number > 0:
            super_punch = randint(1, 6)
            if super_punch == 3:
                boss.damage = 0
                boss.stun = True
                print(f'Boss {boss.name} оглушен героем {self.name} на 1 раунд ')
            else:
                boss.stun = False
                boss.damage = 60


class Saitama(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'ONE_PUNCH')

    def apply_super_power(self, boss, heroes):
        boss.health = 0
        print(f'{self.name} used ONE PUNCH and defeated the Boss!')


class King(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'SUMMON_SAITAMA')

    def attack(self, boss):
        pass

    def apply_super_power(self, boss, heroes):
        global round_number
        summon_chance = randint(1, 10)
        if summon_chance == 1:
            saitama = Saitama('Saitama', 1000, 10000)
            heroes.append(saitama)
            print(f'{self.name} summoned {saitama.name} who will now defeat the Boss!')
            saitama.apply_super_power(boss, heroes)
        else:
            print(f'{self.name} tried to summon Saitama, but failed.')


round_number = 0

def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and hero.ability != boss.defence:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def show_statistics(boss, heroes):
    print(f'ROUND {round_number} -------------')
    print(boss)
    for hero in heroes:
        print(hero)


def start_game():
    boss = Boss('Lord', 2500, 50)
    warrior_1 = Warrior('Brane', 280, 15)
    warrior_2 = Warrior('Alucard', 270, 20)
    magic = Magic('Subaru', 290, 10)
    doc = Medic('Merlin', 250, 5, 15)
    assistant = Medic('Florin', 300, 5, 5)
    berserk = Berserk('Guts', 260, 10)
    witcher = Witcher('Estes', 300, 0)
    hacker = Hacker('Ronaldo', 270, 13)
    thor = Thor('Thor', 260, 10)
    king = King('King', 200, 0)

    heroes_list = [warrior_1, warrior_2, magic, doc, assistant, berserk, witcher, hacker, thor, king]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
