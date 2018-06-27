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
weights = '01-06 Accursed|07-12 Ancient|13-14 Baneful|15-18 Batrachian|19-25 Black|26-28 Bloodstained|29-30 Cold|31-38 Dark|39-40 Devouring|41-42 Diabolical|43-44 Ebon|45-47 Eldritch|48-51 Forbidden|52-55 Forgotten|56-57 Haunted|58-61 Hidden|62-63 Lonely|64-67 Lost|68-69 Malevolent|70-71 Misplaced|72-73 Nameless|74-75 Ophidian|76-77 Scarlet|78-80 Secret|81-82 Shrouded|83-84 Squamous|85-86 Strange|87-88 Tenebrous|89-90 Uncanny|91-92 Unspeakable|93-94 Unvanquishable|95-96 Unwholesome|97-98 Vanishing|99-100 Weird|01-02 Abyss|03-05 Catacombs|06-10 Caverns|11-13 Citadel|14-15 City|16-17 Cyst|18-21 Depths|22-26 Dungeons|27-30 Fane|31-33 Fortress|34-36 Halls|37-38 Haunts|39-40 Isle|41-43 Keep|44-49 Labyrinth|50-53 Manse|54-60 Maze|61-62 Milieu|63-67 Mines|68-71 Mountain|72-74 Oubliette|75-77 Panopticon|78-81 Pits|82-84 Ruins|85-87 Sanctum|88-89 Shambles|90-93 Temple|94-95 Tower|96-100 Vault|01-02 the Axolotl|03-04 Blood|05-06 Bones|07-08 Chaos|09-11 the (Table I) Cult|12-13 Curses|14-15 the Dead|16-17 Death|18-19 Demons|20-21 Despair|22-23 Deviltry|24-25 Doom|26-27 the Dweller(s) in [01-50] the (Table II) [51-00] (Table IV)|28-29 (Table I) Dweomercraeft|30-31 Evil|32-33 Fire|34-35 Frost|36-37 the (3-13) Geases|38-39 Gloom|40-41 Hells|42-43 Horrors|44-45 Ichor|46-47 Id Insinuation|48-49 the (Table I) Idol|50-51 Iron|52-53 Madness|54-55 Mirrors|56-57 Mists|58-59 Monsters|60-61 Mystery|62-63 Necromancy|64-65 Oblivion|66-68 the (Table I) One(s)|69-70 Peril|71-72 Phantasms|73-74 Random Harlots|75-76 Secrets|77-78 Shadows|79-80 Sigils|81-82 Skulls|83-84 Slaughter|85-86 Sorcery|87-88 Syzygy|89-90 Terror|91-92 Torment|93-94 Treasure|95-96 the Undercity|97-98 the Underworld|99-100 the Unknown'

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


if __name__ == '__main__':
    for a in range(100):
        print(gen_random_dungeon_name()) # choice(choice(tables)))
    weights = weights.split('|')
    splitt = {}
    splitt['of'] = 1
    for word in weights:
        name = word[word.index(' ')+1:]
        number = word[:word.index(' ')]
        num1, num2 = number.split('-')
        quan = int(num2) - int(num1) + 1
        splitt[name] = quan
    for table in tables:
        weight = [splitt[a] for a in table]
        print(weight, sum(weight))