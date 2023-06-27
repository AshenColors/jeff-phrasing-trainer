import random
import importlib
jp  = importlib.import_module("jeff-phrasing.jeff-phrasing")

simple_starters_keys = list(jp.SIMPLE_STARTERS.keys())
simple_pronouns_keys = list(jp.SIMPLE_PRONOUNS.keys())
simple_structures_keys = list(jp.SIMPLE_STRUCTURES.keys())

# Ender format: base_ender: (past_form, suffix_form, past_suffix_form)
enders = { 
    "RB": ("RBD", None, None),
    "B": ("BD", "BT", "BTD"),
    "RPBG": ("RPBGD", "RPBGT", "RPBGTD"),
    "BL": ("BLD", "BLT", "BLTD"),
    "RBLG": ("RBLGD", None, None),
    "BGS": ("BGSZ", None, None),
    "RZ": ("RDZ", None, None),
    "BG": ("BGD", "BGT", "BGTD"),
    "RP": ("RPD", "RPT", "RPTD"),
    "PGS": ("PGSZ", "PGTS", "PGTSDZ"),
    "LT": ("LTD", "LTS", "LTSDZ"),
    "PBLG": ("PBLGD", "PBLGT", "PBLGTD"),
    "RG": ("RGD", "RGT", "RGTD"),
    "GS": ("GSZ", "GTS", "GTSDZ"),
    "GZ": ("GDZ", None, None),
    "G": ("GD", "GT", "GTD"),
    "T": ("TD", "TS", "TSDZ"),
    "PZ": ("PDZ", None, None),
    "PG": ("PGD", "PGT", "PGTD"),
    "RPS": ("RPSZ", "RPTS", "RPTSDZ"),
    "PLG": ("PLGD", "PLGT", "PLGTD"),
    "PBLGSZ": ("PBLGTSDZ", None, None),
    "PBGS": ("PBGSZ", None, None),
    "PB": ("PBD", "PBT", "PBTD"),
    "RPBS": ("RPBSZ", "RPBTS", "RPBTSDZ"),
    "LGZ": ("LGDZ", None, None),
    "LS": ("LSZ", None, None),
    "BLG": ("BLGD", "BLGT", "BLGTD"),
    "LZ": ("LDZ", None, None),
    "L": ("LD", None, None),
    "LG": ("LGD", "LGT", "LGTD"),
    "RPBL": ("RPBLD", "RPBLT", "RPBLTD"),
    "PL": ("PLD", "PLT", "PLTD"),
    "PBL": ("PBLD", "PBLT", "PBLTD"),
    "PBLS": ("PBLSZ", None, None),
    "PLZ": ("PLDZ", None, None),
    "PBLGS": (None, "PBLGTS", None),
    "RPG": ("RPGD", "RPGT", "RPGTD"),
    "PS": ("PSZ", "PTS", "PTSDZ"),
    "RS": ("RSZ", None, None),
    "RLG": ("RLGD", None, None),
    "RL": ("RLD", None, None),
    "RLS": ("RLSZ", "RLTS", "RLTSDZ"),
    "RPL": ("RPLD", "RPLT", "RPLTD"),
    "RPLS": ("RPLSZ", None, None),
    "R": ("RD", None, None),
    "BS": ("BSZ", "BTS", "BTSDZ"),
    "S": ("SZ", None, None),
    "BLS": ("BLSZ", None, None),
    "PLS": ("PLSZ", "PLTS", "PLTSDZ"),
    "RBL": ("RBLD", None, None),
    "RBZ": ("RBDZ", None, None),
    "RBT": ("RBTD", None, None),
    "RLT": ("RLTD", None, None),
    "PBG": ("PBGD", "PBGT", "PBGTD"),
    "RT": ("RTD", "RTS", "RTSDZ"),
    "Z": ("DZ", "TZ", "TDZ"),
    "P": ("PD", "PT", "PTD"),
    "RBGZ": ("RBGSZ", None, None),
    "RBS": ("RBSZ", "RBTS", "RBTSDZ"),
    "RBG": ("RGBD", "RBGT", "RBGTD")
}

# Options
base_ending_max_keys = 2
include_past = True
include_suffix = True

def generate_simple_phrase():
    allowed_enders = [k for k, v in enders.items() if len(k) < base_ending_max_keys]
    outline = ""
    outline += random.choice(simple_starters_keys)
    outline += random.choice(simple_pronouns_keys)
    outline += random.choice(simple_structures_keys)
    base_ender = random.choice(allowed_enders)
    possible_ender_variants = [base_ender]
    if include_past and (enders[base_ender][0] is not None):
        possible_ender_variants.append(enders[base_ender][0])
    if include_suffix and (enders[base_ender][1] is not None):
        possible_ender_variants.append(enders[base_ender][1])
    if include_past and include_suffix and (enders[base_ender][2] is not None):
        possible_ender_variants.append(enders[base_ender][2])
    outline += random.choice(possible_ender_variants)
    translation = jp.lookup([outline]).strip()
    reverse_lookup = jp.reverse_lookup(translation)
    return translation + "\t" + (min(reverse_lookup, key=len)[0]) + "\n"

with open("output.txt", 'w') as f:
    for n in range(20):
        f.write(generate_simple_phrase())
