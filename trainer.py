"""
Generates custom lessons based on jeff-phrasing to use with Typey Type.
"""
import random
import argparse
import typing
import importlib

jp = importlib.import_module("jeff-phrasing.jeff-phrasing")

# simple form phrase parts
SIMPLE_STARTERS_KEYS = list(jp.SIMPLE_STARTERS.keys())
SIMPLE_PRONOUNS_KEYS = list(jp.SIMPLE_PRONOUNS.keys())
SIMPLE_STRUCTURES_KEYS = list(jp.SIMPLE_STRUCTURES.keys())

# STKWH for "why" isn't documented and really hard to stroke
# so we're not including it in the list of valids
# yes, that's supposed to be a const, it really is after this
SIMPLE_STARTERS_KEYS.remove("STKWH")

# full form phrase parts
STARTERS_KEYS = list(jp.STARTERS.keys())
MIDDLES_KEYS = list(jp.MIDDLES.keys())
STRUCTURES_KEYS = list(jp.STRUCTURES.keys())

# Ender format: base_ender: (past_form, suffix_form, past_suffix_form)
# Ideally we'd parse this directly from jeff-phrasing but there are
# irregularities that make this a much easier approach for now.
# this is shared by both simple and full form
ENDERS = {
    "RB": ("RBD", None, None),
    "B": ("BD", "BT", "BTD"),
    "RPBG": ("RPBGD", "RPBGT", "RPBGTD"),
    "BL": ("BLD", "BLT", "BLTD"),
    "RBLG": ("RBLGD", None, None),
    "BGS": ("BGSZ", None, None),
    "RZ": ("RDZ", None, None),
    "PBGZ": ("PBGDZ", None, None),
    "BG": ("BGD", "BGT", "BGTD"),
    "RBGZ": ("RBGDZ", None, None),
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
    while True:
        allowed_enders = [k for k, v in ENDERS.items() if len(k) <= args["max"]]
        outline = ""
        outline += random.choice(SIMPLE_STARTERS_KEYS)
        outline += random.choice(SIMPLE_PRONOUNS_KEYS)
        if args["include_simple_have"]:
            outline += random.choice(SIMPLE_STRUCTURES_KEYS)
        base_ender = random.choice(allowed_enders)
        possible_ender_variants = [base_ender]
        if args["include_past"] and (ENDERS[base_ender][0] is not None):
            possible_ender_variants.append(ENDERS[base_ender][0])
        if args["include_suffix_word"] and (ENDERS[base_ender][1] is not None):
            possible_ender_variants.append(ENDERS[base_ender][1])
        if (
            args["include_past"]
            and args["include_suffix_word"]
            and (ENDERS[base_ender][2] is not None)
        ):
            possible_ender_variants.append(ENDERS[base_ender][2])
        outline += random.choice(possible_ender_variants)
        try:
            translation = jp.lookup([outline]).strip()
        except KeyError:
            # We tried an invalid outline, try again
            continue
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


def generate_full_phrase():
    """Generates a full form phrase based on current arguments
    and the corresponding stroke.

    Returns:
        dict: Translation as key and stroke as value.
    """
    while True:
        allowed_enders = [k for k, v in ENDERS.items() if len(k) <= args["max"]]
        outline = ""
        outline += random.choice(STARTERS_KEYS)
        if args["include_middle"]:
            outline += random.choice(MIDDLES_KEYS)
        if args["include_structure"]:
            outline += random.choice(STRUCTURES_KEYS)
        base_ender = random.choice(allowed_enders)
        possible_ender_variants = [base_ender]
        if args["include_past"] and (ENDERS[base_ender][0] is not None):
            possible_ender_variants.append(ENDERS[base_ender][0])
        if args["include_suffix_word"] and (ENDERS[base_ender][1] is not None):
            possible_ender_variants.append(ENDERS[base_ender][1])
        if (
            args["include_past"]
            and args["include_suffix_word"]
            and (ENDERS[base_ender][2] is not None)
        ):
            possible_ender_variants.append(ENDERS[base_ender][2])
        outline += random.choice(possible_ender_variants)
        try:
            translation = jp.lookup([outline]).strip()
        except KeyError:
            # We tried an invalid outline, try again
            continue
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
                + " caused a ValueError, which means this outline "
                + "isn't passing round-trip with reverse_lookup()."
            )
            return {translation: outline}


def make_lesson(lines: int, *phrase_gen: typing.Callable):
    """Make a dict

    Args:
        *phrase_gen (typing.Callable): The phrase generation function to call.
        If more than one, randomly choose between them for each entry.
    """
    lesson = {}
    for _ in range(lines):
        while True:
            candidate = random.choice(phrase_gen)()
            if list(candidate.keys())[0] not in lesson:
                lesson.update(candidate)
                break
    return lesson


def format_lesson(lesson: dict):
    """Prints a lesson in Typey Type custom lesson format.

    Args:
        lesson (dict): The generated lesson to print out.
    """

    for k, v in lesson.items():  # pylint: disable=invalid-name
        print(k + "\t" + v)


argparser = argparse.ArgumentParser(
    "Generate Typey Type compatile custom lessons to "
    + "practice phrases made with the jeff-phrasing "
    + "dictionary for Plover."
)
argparser.add_argument(
    "-n",
    "--lines",
    dest="lines",
    type=int,
    choices=range(1, 100 + 1),
    default=20,
    metavar="N",
    help="Number of lesson entries to generate, from 1 to 100, default 20.",
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
form_group = argparser.add_mutually_exclusive_group()
form_group.add_argument(
    "--simple-only",
    dest="forms",
    action="store_const",
    const=(generate_simple_phrase,),
    default=(generate_simple_phrase, generate_full_phrase),
    help="Only generate simple form phrases.",
)
form_group.add_argument(
    "--full-only",
    dest="forms",
    action="store_const",
    const=(generate_full_phrase,),
    default=(generate_simple_phrase, generate_full_phrase),
    help="Only generate full form phrases.",
)
argparser.add_argument(
    "--no-simple-have",
    dest="include_simple_have",
    action="store_false",
    help="Don't allow the F key in simple form. Doesn't affect the ender 'T'.",
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
argparser.add_argument(
    "--no-full-structure",
    dest="include_structure",
    action="store_false",
    help="Don't allow E, U, or F in full form phrases.",
)
argparser.add_argument(
    "--no-full-middle",
    dest="include_middle",
    action="store_false",
    help="Don't allow A, O, or * in full form phrases.",
)

args = vars(argparser.parse_args())

if args["min"] > args["max"]:
    raise ValueError("Minimum keys cannot be greater than maximum keys!")


format_lesson(make_lesson(args["lines"], *args["forms"]))
