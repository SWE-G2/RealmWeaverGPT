import random

def roll_dice(num_dice, num_sides):
    rolls = []
    for i in range(num_dice):
        rolls.append(random.randint(1, num_sides))
    return rolls if num_dice > 1 else [rolls[0]]
