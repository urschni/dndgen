from random import randint, choices
# Table from http://www.enworld.org/forum/showthread.php?274089-Random-dungeon-name-generator
table1 = ['Accursed', 'Ancient', 'Baneful', 'Batrachian', 'Black', 'Bloodstained', 'Cold', 'Dark', 'Devouring', 'Diabolical', 'Ebon', 'Eldritch', 'Forbidden', 'Forgotten', 'Haunted', 'Hidden', 'Lonely', 'Lost', 'Malevolent', 'Misplaced', 'Nameless', 'Ophidian', 'Scarlet', 'Secret', 'Shrouded', 'Squamous', 'Strange', 'Tenebrous', 'Uncanny', 'Unspeakable', 'Unvanquishable', 'Unwholesome', 'Vanishing', 'Weird']
table1_weights = [6, 6, 2, 4, 7, 3, 2, 8, 2, 2, 2, 3, 4, 4, 2, 4, 2, 4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
table2 = ['Abyss', 'Catacombs', 'Caverns', 'Citadel', 'City', 'Cyst', 'Depths', 'Dungeons', 'Fane', 'Fortress', 'Halls', 'Haunts', 'Isle', 'Keep', 'Labyrinth', 'Manse', 'Maze', 'Milieu', 'Mines', 'Mountain', 'Oubliette', 'Panopticon', 'Pits', 'Ruins', 'Sanctum', 'Shambles', 'Temple', 'Tower', 'Vault']
table2_weights = [2, 3, 5, 3, 2, 2, 4, 5, 4, 3, 3, 2, 2, 3, 6, 4, 7, 2, 5, 4, 3, 3, 4, 3, 3, 2, 4, 2, 5]
table3 = ['of']
table3_weights = [1]
table4 = ['the Axolotl', 'Blood', 'Bones', 'Chaos', 'the (Table I) Cult', 'Curses', 'the Dead', 'Death', 'Demons', 'Despair', 'Deviltry', 'Doom', '(Table I) Dweomercraeft', 'Evil', 'Fire', 'Frost', 'the (3-13) Geases', 'Gloom', 'Hells', 'Horrors', 'Ichor', 'Id Insinuation', 'the (Table I) Idol', 'Iron', 'Madness', 'Mirrors', 'Mists', 'Monsters', 'Mystery', 'Necromancy', 'Oblivion', 'the (Table I) One(s)', 'Peril', 'Phantasms', 'Random Harlots', 'Secrets', 'Shadows', 'Sigils', 'Skulls', 'Slaughter', 'Sorcery', 'Syzygy', 'Terror', 'Torment', 'Treasure', 'the Undercity', 'the Underworld', 'the Unknown']
table4_weights = [2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
tables = [table1, table2, table3, table4]
tables_weights = [table1_weights, table2_weights, table3_weights, table4_weights]


def gen_random_dungeon_name():
    dungeon_name = ['The']
    for a in range(len(tables)):
        dungeon_name.append(choices(tables[a], weights=tables_weights[a], k=1)[0])
    for a in range(len(dungeon_name)):
        part = dungeon_name[a]
        part = part.replace('(Table I)', choices(table1, weights=table1_weights)[0])
        part = part.replace('(Table II)', choices(table2, weights=table2_weights)[0])
        part = part.replace('(3-13)', str(randint(3, 13)))
        part = part.replace('(s)', '')
        dungeon_name[a] = part
    return ' '.join(dungeon_name)
