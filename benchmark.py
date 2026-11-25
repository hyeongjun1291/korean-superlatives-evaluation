"""한국어 최상급 문항의 조사, 문장 틀, 실험 당시의 문항 번호."""

def particle(word, final, open_):
    has_final = (ord(word[-1]) - ord("가")) % 28 != 0
    return word + (final if has_final else open_)


def quantity_sentences(slot):
    """수량 문항 한 묶음의 전제 두 개와 가설 두 개를 만든다."""
    noun = particle(slot["noun"], "을", "를")
    past, relative = ("읽었다", "읽은") if slot["verb_family"] == "read" else ("모았다", "모은")
    premises = {
        "nominal": f"철수가 가장 많은 {noun} {past}.",
        "adverbial": f"철수가 {noun} 가장 많이 {past}.",
    }
    hypotheses = {
        "category": f"철수는 자신이 {relative} 다른 종류의 {slot['category']}보다 {noun} 더 많이 {past}.",
        "person": f"철수는 다른 사람들보다 {noun} 더 많이 {past}.",
    }
    return premises, hypotheses


def creation_sentences(slot, forms, benefactive):
    noun = slot["noun"]
    obj = particle(noun, "을", "를")
    price = slot["family"] == "price_gift"
    agent = "buyer" if price else "agent"
    category = "product" if price else "category"
    if benefactive:
        premises = {
            "nominal": f"철수가 영희에게 가장 {forms['adnom']} {obj} {forms['ben']}.",
            "adverbial": f"철수가 영희에게 {obj} 가장 {forms['adv']} {forms['ben']}.",
        }
        start = f"철수가 영희에게 {forms['brel']} {particle(noun, '은', '는')} "
        comparisons = {
            agent: f"다른 사람들이 영희에게 {forms['brel']} {noun}",
            "recipient": f"철수가 다른 사람들에게 {forms['brel']} {noun}",
            category: f"그가 영희에게 {forms['brel']} 다른 종류의 {forms['category']}",
        }
        hypotheses = {target: f"{start}{comparison}보다 {forms['adj']}."
                      for target, comparison in comparisons.items()}
    else:
        premises = {
            "nominal": f"철수가 가장 {forms['adnom']} {obj} {forms['past']}.",
            "adverbial": f"철수가 {obj} 가장 {forms['adv']} {forms['past']}.",
        }
        other_types = "물건" if price else forms["category"]
        hypotheses = {
            agent: f"철수는 다른 사람들보다 {obj} 더 {forms['adv']} {forms['past']}.",
            category: f"철수는 자신이 {forms['rel']} 다른 종류의 {other_types}보다 {obj} 더 {forms['adv']} {forms['past']}.",
        }
    return premises, hypotheses


def possession_sentences(slot):
    band, noun = slot["band"], slot["noun"]
    subj = particle(noun, "이", "가")
    obj = particle(f"{band}의 {noun}", "을", "를")
    premises = {
        "nominal": f"철수가 가장 많은 {band}의 {subj} 있다.",
        "predicative": f"철수가 {band}의 {subj} 가장 많다.",
    }
    hypotheses = {
        "owner": f"철수는 다른 사람들보다 {obj} 더 많이 가지고 있다.",
        "band": f"철수는 다른 밴드의 {noun}보다 {obj} 더 많이 가지고 있다.",
        "product": f"철수는 {band}의 다른 종류의 상품보다 {obj} 더 많이 가지고 있다.",
    }
    return premises, hypotheses


def construction_templates(slot, scales, quantity_template):
    family = slot["family"]
    if family == "quantity":
        yield "quantity", False, quantity_template(slot)
    elif family == "possession":
        yield "possession", False, possession_sentences(slot)
    else:
        for benefactive in (False, True):
            module = ("gift" if benefactive else "price") if family == "price_gift" else family
            forms = scales["gift" if family == "price_gift" else family]
            yield module, benefactive, creation_sentences(slot, forms, benefactive)


def identifiers(slot, module, benefactive, target, structure):
    """기존 응답과 연결할 수 있도록 자료를 만들 때 붙였던 번호를 사용한다."""
    group = slot["group"]
    suffix = {"nominal": "NOM", "adverbial": "ADV", "predicative": "PRED"}[structure]
    role = target.upper()
    if slot["stage"] == "후속 증강":
        if module == "possession":
            return f"V9-POSS-{group}-{role}-{suffix}", f"v9-possession-{group}-{target}"
        block, pair = ("BEN", "benefactive") if benefactive else ("CORE", "simple")
        return f"V9-{block}-{group}-{role}-{suffix}", f"v9-{pair}-{group}-{target}"
    if module == "possession":
        base = "POSS" if group == "POSS-U2" else f"POSS-{group}"
        return f"{base}-{suffix}-{role}", f"possession-{group}-{target}"
    if benefactive:
        block = "ROLE" if module == "gift" else "BEN"
        base = f"{block}-{group}-{role}"
        return base if structure == "nominal" else base+"-ADV", f"v9-benefactive-{group}-{target}"
    block = "CORE" if target in ("category", "product") else "CONTROL"
    pair = f"{module}-{group}-{target}" if module in ("price", "quantity") else f"{group}-{target}"
    return f"{block}-{group}-{suffix}", pair


def item_row(slot, module, benefactive, target, form, premise, hypothesis, key):
    item_id, pair_id = identifiers(slot, module, benefactive, target, form)
    return {"id": item_id, "pair_id": pair_id, "premise": premise, "hypothesis": hypothesis,
            "structure": form, "comparison_target": target, "key": key, "module": module,
            "lexical_group_id": slot["group"], "noun": slot["noun"]}
