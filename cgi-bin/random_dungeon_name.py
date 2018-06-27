from random import randint, choice
# Table from http://www.enworld.org/forum/showthread.php?274089-Random-dungeon-name-generator
table1 = ['Accursed', 'Ancient', 'Baneful', 'Batrachian', 'Black', 'Bloodstained', 'Cold', 'Dark', 'Devouring', 'Diabolical', 'Ebon', 'Eldritch', 'Forbidden', 'Forgotten', 'Haunted', 'Hidden', 'Lonely', 'Lost', 'Malevolent', 'Misplaced', 'Nameless', 'Ophidian', 'Scarlet', 'Secret', 'Shrouded', 'Squamous', 'Strange', 'Tenebrous', 'Uncanny', 'Unspeakable', 'Unvanquishable', 'Unwholesome', 'Vanishing', 'Weird']
table2 = ['Abyss', 'Catacombs', 'Caverns', 'Citadel', 'City', 'Cyst', 'Depths', 'Dungeons', 'Fane', 'Fortress', 'Halls', 'Haunts', 'Isle', 'Keep', 'Labyrinth', 'Manse', 'Maze', 'Milieu', 'Mines', 'Mountain', 'Oubliette', 'Panopticon', 'Pits', 'Ruins', 'Sanctum', 'Shambles', 'Temple', 'Tower', 'Vault']
table3 = ['of']
table4 = ['the Axolotl', 'Blood', 'Bones', 'Chaos', 'the (Table I) Cult', 'Curses', 'the Dead', 'Death', 'Demons', 'Despair', 'Deviltry', 'Doom', '(Table I) Dweomercraeft', 'Evil', 'Fire', 'Frost', 'the (3-13) Geases', 'Gloom', 'Hells', 'Horrors', 'Ichor', 'Id Insinuation', 'the (Table I) Idol', 'Iron', 'Madness', 'Mirrors', 'Mists', 'Monsters', 'Mystery', 'Necromancy', 'Oblivion', 'the (Table I) One(s)', 'Peril', 'Phantasms', 'Random Harlots', 'Secrets', 'Shadows', 'Sigils', 'Skulls', 'Slaughter', 'Sorcery', 'Syzygy', 'Terror', 'Torment', 'Treasure', 'the Undercity', 'the Underworld', 'the Unknown']
tables = [table1, table2, table3, table4]


def gen_random_dungeon_name():
    dungeon_name = ['The']
    for table in tables:
        dungeon_name.append(choice(table))
    for a in range(len(dungeon_name)):
        part = dungeon_name[a]
        part = part.replace('(Table I)', choice(table1))
        part = part.replace('(Table II)', choice(table2))
        part = part.replace('(3-13)', str(randint(3, 13)))
        part = part.replace('(s)', '')
        dungeon_name[a] = part
    return ' '.join(dungeon_name)


if __name__ == '__main__':
    for a in range(100):
        print(gen_random_dungeon_name()) # choice(choice(tables)))