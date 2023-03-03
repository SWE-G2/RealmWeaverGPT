import func.dice as dice

class Character:
    def __init__(self, name, race, char_class, age, gear, weapons, spells, ability_scores, hp, extra_info):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.age = age
        self.gear = gear
        self.weapons = weapons
        self.spells = spells
        self.ability_scores = ability_scores
        self.hp = hp
        self.extra_info = extra_info
        self.hit_dice = self.get_class_hit_dice()
        self.hp = self.calculate_hp()

    def get_class_hit_dice(self):
        hit_dice = {
            'Barbarian': 12,
            'Bard': 8,
            'Cleric': 8,
            'Druid': 8,
            'Fighter': 10,
            'Monk': 8,
            'Paladin': 10,
            'Ranger': 10,
            'Rogue': 8,
            'Sorcerer': 6,
            'Warlock': 8,
            'Wizard': 6
        }
        if self.char_class is not 'Barbarian' or 'Bard' or 'Cleric' or 'Druid' or 'Figther' or 'Monk' or 'Paladin' or 'Ranger' or 'Sorcerer' or 'Warlock' or 'Wizard':
            hit_dice = 8
        return hit_dice(self.char_class)

    def calculate_hp(self):
        con_mod = self.calculate_modifier(self.ability_scores['Constitution'])
        hit_dice_value = dice.roll_dice(1, self.hit_dice)
        return hit_dice_value + con_mod

    @staticmethod
    def calculate_modifier(ability_score):
        return (ability_score - 10) // 2

    def to_dict(self):
        return {
            'name': self.name,
            'race': self.race,
            'char_class': self.char_class,
            'age': self.age,
            'gear': self.gear,
            'weapons': self.weapons,
            'spells': self.spells,
            'ability_scores': self.ability_scores,
            'extra_info': self.extra_info,
            'hp': self.hp
        }
