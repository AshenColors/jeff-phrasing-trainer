"""
Generates custom lessons based on jeff-phrasing to use with Typey Type.
"""
import random
import argparse
import importlib

jp = importlib.import_module("jeff-phrasing.jeff-phrasing")

argparser = argparse.ArgumentParser(
    "Generate Typey Type compatile custom lessons to\
                                 practice phrases made with the jeff-phrasing\
                                 dictionary for Plover."
)
argparser.add_argument(
    "-n",
    "--lines",
    dest="lines",
    type=int,
    choices=range(1, 100 + 1),
    default=20,
    metavar="N",
    help="Number of lesson entries to generate, from 1 to 100",
)
argparser.add_argument(
    "--min",
    dest="min",
    type=int,
    choices=range(1, 6),
    default=1,
    help="Minimum number of keys in the base ender for each phrase.",
)
argparser.add_argument(
    "--max",
    dest="max",
    type=int,
    choices=range(1, 7),
    default=7,
    help="Maximum number of keys in the base ender for each phrase.",
)
argparser.add_argument(
    "--no-have",
    dest="include_have",
    action="store_false",
    help="Don't allow the F key in strokes. Doesn't affect the ender 'T'.",
)
argparser.add_argument(
    "--no-past",
    dest="include_past",
    action="store_false",
    help="Don't allow past tense in phrases.",
)
argparser.add_argument(
    "--no-suffix-word",
    dest="include_suffix_word",
    action="store_false",
    help="Don't allow suffix words in phrases.",
)

args = vars(argparser.parse_args())

# could probably just read directly from the dict when needed,
# maybe refactor this later
lines = args["lines"]
base_ender_min_keys = args["min"]
base_ender_max_keys = args["max"]
include_have = args["include_have"]
include_past = args["include_past"]
include_suffix_word = args["include_suffix_word"]

if base_ender_min_keys > base_ender_max_keys:
    raise ValueError("Minimum keys cannot be greater than maximum keys!")

simple_starters_keys = list(jp.SIMPLE_STARTERS.keys())
simple_pronouns_keys = list(jp.SIMPLE_PRONOUNS.keys())
simple_structures_keys = list(jp.SIMPLE_STRUCTURES.keys())

# STKWH for "why" isn't documented and really hard to stroke
simple_starters_keys.remove("STKWH")

# Ender format: base_ender: (past_form, suffix_form, past_suffix_form)
# Ideally we'd parse this directly from jeff-phrasing but there are
# irregularities that make this a much easier approach for now.
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
    "RBG": ("RGBD", "RBGT", "RBGTD"),
}


def generate_simple_phrase():
    """Generates a simple form phrase based on current arguments
    and the corresponding stroke.

    Returns:
        dict: Translation as key and stroke as value.
    """
    allowed_enders = [k for k, v in enders.items() if len(k) <= base_ender_max_keys]
    outline = ""
    outline += random.choice(simple_starters_keys)
    outline += random.choice(simple_pronouns_keys)
    if include_have:
        outline += random.choice(simple_structures_keys)
    base_ender = random.choice(allowed_enders)
    possible_ender_variants = [base_ender]
    if include_past and (enders[base_ender][0] is not None):
        possible_ender_variants.append(enders[base_ender][0])
    if include_suffix_word and (enders[base_ender][1] is not None):
        possible_ender_variants.append(enders[base_ender][1])
    if include_past and include_suffix_word and (enders[base_ender][2] is not None):
        possible_ender_variants.append(enders[base_ender][2])
    outline += random.choice(possible_ender_variants)
    translation = jp.lookup([outline]).strip()
    # Sanity check; make sure we're actually using the shortest stroke for this translation
    # Can occur if we have past tense on an ender that outputs identical text[]
    reverse_lookup = jp.reverse_lookup(translation)
    try:
        return {translation: min(reverse_lookup, key=len)[0]}
    except ValueError:
        # The bug this checks for has been resolved, but I'm leaving this in as a sanity check.
        print(
            "generated "
            + outline
            + " caused a ValueError, which means this outline\
              isn't passing round-trip with reverse_lookup()."
        )
        return {translation: outline}


lesson = {}
for n in range(lines):
    while True:
        candidate = generate_simple_phrase()
        if list(candidate.keys())[0] not in lesson:
            lesson.update(candidate)
            break

for k, v in lesson.items():
    print(k + "\t" + v)
