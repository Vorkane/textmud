

LEVEL = {
    '1': {'xp': 100},
    '2': {'xp': 200},
    '3': {'xp': 500},
    '4': {'xp': 700},
    '5': {'xp': 900},
}


def item_durability(item):
    current = item.db.curr_dura
    max_durability = item.db.max_dura

    if max_durability > 0:
        percent = int(current / max_durability * 100)
    else:
        percent = 0

    if percent == 100:
        return 'Is in |040perfect condition|n'
    if percent > 75:
        return 'Is |530slightly damaged|n'
    if percent > 50:
        return 'Is |520moderately damaged|n'
    if percent > 25:
        return 'Is |510severly damaged|n'
    if percent > 10:
        return '|500Needs repair!|n'
    else:
        return ''
