import json
import random

with open("card_packs.json", "r", encoding='utf-8') as f:
    card_packs = json.loads(f.read())


def get_card(color: str, pack_code: int = -1, n: int = 1) -> {str: any}:
    """
    :param n: number of cards to be returned (maximum: 1000)
    :param color: black/white
    :param pack_code:  of the pack (default is "-1" and it means pick a random pack)
    :return: a string containing the text of a random card from the selected pack
    """
    if n > 1000:
        raise ValueError("Number of cards should be less than 1000")
    results = []
    random_pack = pack_code == -1
    for i in range(n):
        res = {}
        while res in results or not res:
            try:
                if random_pack:
                    pack_code = random.randint(0, len(card_packs) - 1)
                res['pack'] = card_packs[pack_code]['name']
                res['text'] = card_packs[pack_code][color][random.randint(0, len(card_packs[pack_code][color]) - 1)]['text']
            except Exception as e:
                res = {}

        results.append(res)

    return results
