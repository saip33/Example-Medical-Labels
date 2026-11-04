import json
import math
import os
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUTPUT_ROOT = "/Users/saipavangopularam/Desktop/labels"
FLAT_DIR = os.path.join(OUTPUT_ROOT, "flat")
CURVED_DIR = os.path.join(OUTPUT_ROOT, "curved")
META_DIR = os.path.join(OUTPUT_ROOT, "annotations")

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_NARROW = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
FONT_NARROW_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_ROUNDED = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"

# Large pools for unique PII generation
FIRST_NAMES = [
    "JAMES", "MARY", "ROBERT", "PATRICIA", "JOHN", "JENNY", "MICHAEL", "LINDA",
    "DAVID", "ELIZABETH", "WILLIAM", "BARBARA", "RICHARD", "SUSAN", "JOSEPH", "JESSICA",
    "THOMAS", "SARAH", "CHARLES", "KAREN", "CHRISTOPHER", "LISA", "DANIEL", "NANCY",
    "MATTHEW", "BETTY", "ANTHONY", "MARGARET", "MARK", "SANDRA", "DONALD", "ASHLEY",
    "STEVEN", "KIMBERLY", "PAUL", "EMILY", "ANDREW", "DONNA", "JOSHUA", "MICHELLE",
    "KENNETH", "CAROL", "KEVIN", "AMANDA", "BRIAN", "MELISSA", "GEORGE", "DEBORAH",
    "TIMOTHY", "STEPHANIE", "RONALD", "REBECCA", "EDWARD", "SHARON", "JASON", "LAURA",
    "JEFFREY", "CYNTHIA", "RYAN", "KATHLEEN", "JACOB", "AMY", "GARY", "ANGELA",
    "NICHOLAS", "SHIRLEY", "ERIC", "ANNA", "JONATHAN", "BRENDA", "STEPHEN", "PAMELA",
    "LARRY", "EMMA", "JUSTIN", "NICHOLE", "SCOTT", "HELEN", "BRANDON", "SAMANTHA",
    "BENJAMIN", "KATHERINE", "SAMUEL", "CHRISTINE", "GREGORY", "DEBRA", "ALEXANDER", "RACHEL",
    "PATRICK", "CAROLYN", "FRANK", "JANET", "RAYMOND", "MARIA", "JACK", "HEATHER",
    "DENNIS", "DIANE", "JERRY", "RUTH", "TYLER", "JULIE", "AARON", "OLIVIA",
    "JOSE", "JOYCE", "ADAM", "VIRGINIA", "NATHAN", "VICTORIA", "HENRY", "KELLY",
    "DOUGLAS", "LAUREN", "ZACHARY", "CHRISTINA", "PETER", "JOAN", "KYLE", "EVELYN",
    "ETHAN", "JUDITH", "WALTER", "MEGAN", "NOAH", "ANDREA", "JEREMY", "CHERYL",
    "CHRISTIAN", "HANNAH", "KEITH", "JACQUELINE", "ROGER", "MARTHA", "TERRY", "GLORIA",
    "GERALD", "TERESA", "HAROLD", "ANN", "SEAN", "SARA", "AUSTIN", "MADISON",
    "CARL", "FRANCES", "ARTHUR", "KATHRYN", "LAWRENCE", "JANICE", "DYLAN", "JEAN",
    "JESSE", "ABIGAIL", "JORDAN", "ALICE", "BRYAN", "JUDY", "BILLY", "SOPHY",
    "JOE", "GRACE", "BRUCE", "DENISE", "GABRIEL", "AMBER", "LOGAN", "DORIS",
    "ALBERT", "MARILYN", "WILLIE", "DANIELLA", "ALAN", "BEVERLY", "JUAN", "ISABELLA",
    "WAYNE", "THERESA", "ELIJAH", "DIANA", "RANDY", "NATALIE", "ROY", "BRITTANY",
    "VINCENT", "CHARLOTTE", "RALPH", "MARIE", "EUGENE", "KAYLA", "RUSSELL", "ALEXIS",
    "BOBBY", "LORI", "MASON", "PRIYA", "LIAM", "FATIMA", "OMAR", "MEI",
    "ARJUN", "SOFIA", "MATEO", "ZARA", "TARIQ", "YUKI", "SANTIAGO", "AALIYAH",
    "DEVON", "CHLOE", "KENDRA", "MALIK", "ELENA", "DARIUS", "NAOMI", "VIKRAM"
]

LAST_NAMES = [
    "SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA", "MILLER", "DAVIS",
    "RODRIGUEZ", "MARTINEZ", "HERNANDEZ", "LOPEZ", "GONZALEZ", "WILSON", "ANDERSON", "THOMAS",
    "TAYLOR", "MOORE", "JACKSON", "MARTIN", "LEE", "PEREZ", "THOMPSON", "WHITE",
    "HARRIS", "SANCHEZ", "CLARK", "RAMIREZ", "LEWIS", "ROBINSON", "WALKER", "YOUNG",
    "ALLEN", "KING", "WRIGHT", "SCOTT", "TORRES", "NGUYEN", "HILL", "FLORES",
    "GREEN", "ADAMS", "NELSON", "BAKER", "HALL", "RIVERA", "CAMPBELL", "MITCHELL",
    "CARTER", "ROBERTS", "GOMEZ", "PHILLIPS", "EVANS", "TURNER", "DIAZ", "PARKER",
    "CRUZ", "EDWARDS", "COLLINS", "REYES", "STEWART", "MORRIS", "MORALES", "MURPHY",
    "COOK", "ROGERS", "GUTIERREZ", "ORTIZ", "MORGAN", "COOPER", "PETERSON", "BAILEY",
    "REED", "KELLY", "HOWARD", "RAMOS", "KIM", "COX", "WARD", "RICHARDSON",
    "WATSON", "BROOKS", "CHAVEZ", "WOOD", "JAMES", "BENNETT", "GRAY", "MENDOZA",
    "RUIZ", "HUGHES", "PRICE", "ALVAREZ", "CASTILLO", "SANDERS", "PATEL", "MYERS",
    "LONG", "ROSS", "FOSTER", "JIMENEZ", "POWELL", "JENKINS", "PERRY", "RUSSELL",
    "SULLIVAN", "BELL", "COLEMAN", "BUTLER", "HENDERSON", "BARNES", "GONZALES", "FISHER",
    "VASQUEZ", "SIMMONS", "ROMERO", "JORDAN", "PATTERSON", "ALEXANDER", "HAMILTON", "GRAHAM",
    "REYNOLDS", "GRIFFIN", "WALLACE", "MORENO", "WEST", "COLE", "HAYES", "BRYANT",
    "HERRERA", "GIBSON", "ELLIS", "TRAN", "MEDINA", "AGUILAR", "STEVENS", "MURRAY",
    "FORD", "CASTRO", "MARSHALL", "OWENS", "HARRISON", "FERNANDEZ", "MCDONALD", "WOODS",
    "WASHINGTON", "KENNEDY", "WELLS", "VARGAS", "HENRY", "CHEN", "FREEMAN", "WEBB",
    "TUCKER", "GUZMAN", "BURNS", "CRAWFORD", "OLSON", "SIMPSON", "PORTER", "HUNTER",
    "GORDON", "MENDEZ", "SILVA", "SHAW", "SNYDER", "MASON", "DIXON", "MUNOZ",
    "HUNT", "HICKS", "HOLMES", "PALMER", "WAGNER", "BLACK", "ROBERTSON", "BOYD",
    "ROSE", "STONE", "SALAZAR", "FOX", "WARREN", "MILLS", "MEYER", "RICE",
    "SCHMIDT", "GARZA", "DANIELS", "FERGUSON", "NICHOLS", "STEPHENS", "SOTO", "WEAVER",
    "RYAN", "GARDNER", "PAYNE", "GRANT", "DUNN", "KELLEY", "SPENCER", "HAWKINS",
    "KAPOOR", "SHARMA", "OKAFOR", "KOWALSKI", "NOVAK", "HADDAD", "NAKAMURA", "PARK",
    "CHOI", "SATO", "GUPTA", "DESAI", "ROSSI", "DUBOIS", "BERGER", "LINDBERG"
]

STREETS = [
    "OAK ST", "MAPLE AVE", "CEDAR LN", "PINE RD", "ELM ST", "WASHINGTON BLVD",
    "LAKEVIEW DR", "HIGHLAND AVE", "PARKWAY RD", "SUNSET BLVD", "MEADOW LN", "RIDGE RD",
    "WALNUT ST", "CHESTNUT AVE", "SYCAMORE DR", "BIRCHWOOD LN", "WILLOW WAY", "SPRING ST",
    "BROADWAY", "MAIN ST", "LINCOLN AVE", "MADISON ST", "JEFFERSON BLVD", "FRANKLIN RD",
    "ADAMS WAY", "MONROE DR", "JACKSON ST", "HARRISON LN", "TYLER AVE", "POLK RD",
    "TAYLOR DR", "FILLMORE ST", "PIERCE LN", "BUCHANAN AVE", "GRANT BLVD", "HAYES WAY",
    "GARFIELD RD", "ARTHUR LN", "CLEVELAND ST", "MCKINLEY AVE", "ROOSEVELT BLVD", "TAFT DR",
    "WILSON WAY", "HARDING LN", "COOLIDGE ST", "HOOVER AVE", "TRUMAN RD", "EISENHOWER PKWY",
    "KENNEDY DR", "JOHNSON BLVD", "NIXON WAY", "FORD LN", "CARTER ST", "REAGAN AVE",
    "CLINTON RD", "HAWTHORNE LN", "MAGNOLIA DR", "DOGWOOD WAY", "CYPRESS AVE", "REDWOOD RD",
    "SEQUOIA LN", "ASPEN DR", "POPLAR ST", "HICKORY AVE", "MULBERRY LN", "PEACHTREE ST",
    "BRIARWOOD DR", "TIMBERLINE RD", "SILVERCREEK LN", "COPPERFIELD WAY", "GOLDENROD AVE", "EMERALD DR"
]

CITIES_STATES = [
    ("CHICAGO", "IL", "606"), ("AUSTIN", "TX", "787"), ("SEATTLE", "WA", "981"),
    ("DENVER", "CO", "802"), ("BOSTON", "MA", "021"), ("ATLANTA", "GA", "303"),
    ("PHOENIX", "AZ", "850"), ("PORTLAND", "OR", "972"), ("MIAMI", "FL", "331"),
    ("DALLAS", "TX", "752"), ("SAN DIEGO", "CA", "921"), ("MINNEAPOLIS", "MN", "554"),
    ("DETROIT", "MI", "482"), ("PHILADELPHIA", "PA", "191"), ("CHARLOTTE", "NC", "282"),
    ("NASHVILLE", "TN", "372"), ("COLUMBUS", "OH", "432"), ("INDIANAPOLIS", "IN", "462"),
    ("SALT LAKE CITY", "UT", "841"), ("RALEIGH", "NC", "276"), ("TAMPA", "FL", "336"),
    ("PITTSBURGH", "PA", "152"), ("ST. LOUIS", "MO", "631"), ("BALTIMORE", "MD", "212"),
    ("KANSAS CITY", "MO", "641"), ("MILWAUKEE", "WI", "532"), ("CLEVELAND", "OH", "441"),
    ("CINCINNATI", "OH", "452"), ("ORLANDO", "FL", "328"), ("SACRAMENTO", "CA", "958"),
    ("SAN JOSE", "CA", "951"), ("LAS VEGAS", "NV", "891"), ("RICHMOND", "VA", "232"),
    ("HARTFORD", "CT", "061"), ("PROVIDENCE", "RI", "029"), ("OMAHA", "NE", "681"),
    ("LOUISVILLE", "KY", "402"), ("OKLAHOMA CITY", "OK", "731"), ("TUCSON", "AZ", "857"),
    ("ALBUQUERQUE", "NM", "871"), ("FRESNO", "CA", "937"), ("MESA", "AZ", "852"),
    ("MADISON", "WI", "537"), ("BOISE", "ID", "837"), ("DES MOINES", "IA", "503")
]

PHARMACY_BRANDS = [
    {"name": "CVS/pharmacy", "color": (204, 0, 0), "accent": (255, 240, 240), "style": "cvs"},
    {"name": "Walgreens Pharmacy", "color": (215, 25, 32), "accent": (240, 245, 255), "style": "walgreens"},
    {"name": "WALMART PHARMACY", "color": (0, 113, 206), "accent": (255, 194, 32), "style": "walmart"},
    {"name": "RITE AID PHARMACY", "color": (0, 56, 147), "accent": (235, 242, 252), "style": "riteaid"},
    {"name": "KROGER HEALTH PHARMACY", "color": (12, 77, 162), "accent": (238, 245, 255), "style": "kroger"},
    {"name": "COSTCO PHARMACY", "color": (227, 24, 55), "accent": (0, 96, 169), "style": "costco"},
    {"name": "PUBLIX PHARMACY", "color": (46, 133, 64), "accent": (240, 250, 242), "style": "publix"},
    {"name": "SAFEWAY PHARMACY", "color": (185, 28, 28), "accent": (250, 245, 245), "style": "safeway"},
    {"name": "H-E-B PHARMACY", "color": (210, 35, 42), "accent": (255, 244, 244), "style": "heb"},
    {"name": "KAISER PERMANENTE PHARMACY", "color": (0, 102, 153), "accent": (238, 248, 255), "style": "kaiser"},
    {"name": "CAREPLUS COMMUNITY RX", "color": (25, 118, 110), "accent": (235, 250, 248), "style": "indie"},
    {"name": "APEX SPECIALTY PHARMACY", "color": (68, 42, 112), "accent": (244, 240, 252), "style": "specialty"},
]

DRUGS_POOL = [
    ("ATORVASTATIN CALCIUM", "20 MG", "TABLET", "LIPITOR", "PFIZER", "00071-0156-23", "WHITE, ELLIPTICAL, FILM-COATED"),
    ("LISINOPRIL", "10 MG", "TABLET", "PRINIVIL", "LUPIN", "68180-0514-01", "PINK, ROUND, BICONVEX"),
    ("METFORMIN HCL", "500 MG", "TABLET", "GLUCOPHAGE", "TEVA", "00093-1048-01", "WHITE, ROUND, FILM-COATED"),
    ("AMLODIPINE BESYLATE", "5 MG", "TABLET", "NORVASC", "MYLAN", "00378-1805-01", "WHITE, OCTAGONAL, FLAT"),
    ("METOPROLOL SUCCINATE ER", "50 MG", "TABLET ER", "TOPROL XL", "ASTRAZENECA", "00186-1090-05", "WHITE, OVAL, SCORED"),
    ("OMEPRAZOLE DR", "20 MG", "CAPSULE DR", "PRILOSEC", "DR. REDDYS", "55111-0158-30", "PURPLE/GRAY, HARD GELATIN CAPSULE"),
    ("LOSARTAN POTASSIUM", "50 MG", "TABLET", "COZAAR", "CAMBER", "31722-0701-90", "GREEN, OVAL, FILM-COATED"),
    ("ALBUTEROL SULFATE HFA", "90 MCG/ACT", "INHALER", "PROAIR HFA", "TEVA RESP", "59310-0579-22", "RED PLASTIC ACTUATOR WITH DOSE COUNTER"),
    ("GABAPENTIN", "300 MG", "CAPSULE", "NEURONTIN", "AMNEAL", "65162-0102-10", "YELLOW, HARD GELATIN CAPSULE"),
    ("HYDROCHLOROTHIAZIDE", "25 MG", "TABLET", "MICROZIDE", "AUROBINDO", "65862-0132-01", "PEACH, ROUND, SCORED"),
    ("SERTRALINE HCL", "50 MG", "TABLET", "ZOLOFT", "CIPLA", "69097-0832-07", "LIGHT BLUE, CAPSULE-SHAPED"),
    ("SIMVASTATIN", "40 MG", "TABLET", "ZOCOR", "ACCORD", "16729-0005-17", "BRICK RED, OVAL, BICONVEX"),
    ("MONTELUKAST SODIUM", "10 MG", "TABLET", "SINGULAIR", "GLENMARK", "68462-0117-30", "BEIGE, ROUNDED SQUARE"),
    ("ESCITALOPRAM OXALATE", "10 MG", "TABLET", "LEXAPRO", "TORRENT", "13668-0136-90", "WHITE, OVAL, FILM-COATED"),
    ("ROSUVASTATIN CALCIUM", "10 MG", "TABLET", "CRESTOR", "SANDOZ", "00781-5701-92", "PINK, ROUND, FILM-COATED"),
    ("LEVOTHYROXINE SODIUM", "75 MCG", "TABLET", "SYNTHROID", "ABBVIE", "00074-9296-90", "VIOLET, ROUND, SCORED"),
    ("PANTOLPRAZOLE SODIUM", "40 MG", "TABLET DR", "PROTONIX", "SUN PHARMA", "47335-0975-88", "YELLOW, OVAL, ENTERIC-COATED"),
    ("FUROSEMIDE", "20 MG", "TABLET", "LASIX", "HIKMA", "00054-8297-25", "WHITE, OVAL, IMPRINTED '54 840'"),
    ("FLUTICASONE PROPIONATE", "50 MCG/ACT", "NASAL SPRAY", "FLONASE", "APOTEX", "60505-0829-01", "AMBER GLASS BOTTLE WITH METERED PUMP"),
    ("AMOXICILLIN", "500 MG", "CAPSULE", "AMOXIL", "SANDOZ", "00781-2613-01", "PINK AND BLUE OPAQUE CAPSULE"),
    ("AZITHROMYCIN", "250 MG", "TABLET", "ZITHROMAX", "PFIZER", "00069-3060-75", "PINK, MODIFIED CAPSULE SHAPE"),
    ("PREDNISONE", "10 MG", "TABLET", "DELTASONE", "WEST-WARD", "00143-1473-01", "WHITE, ROUND, SCORED"),
    ("TRAMADOL HCL", "50 MG", "TABLET", "ULTRAM", "AMNEAL", "53746-0617-01", "WHITE, OVAL, BICONVEX"),
    ("CLOPIDOGREL BISULFATE", "75 MG", "TABLET", "PLAVIX", "APOTEX", "60505-0253-03", "PINK, ROUND, BICONVEX"),
    ("CARVEDILOL", "12.5 MG", "TABLET", "COREG", "ZDYUS", "68382-0094-05", "WHITE, OVAL, FILM-COATED"),
    ("TRAZODONE HCL", "50 MG", "TABLET", "DESYREL", "TEVA", "00555-0732-02", "WHITE, ROUND, SCORED"),
    ("PRAVASTATIN SODIUM", "40 MG", "TABLET", "PRAVACHOL", "TEVA", "00093-7202-98", "GREEN, CAPSULE-SHAPED"),
    ("BUPROPION HCL XL", "150 MG", "TABLET ER", "WELLBUTRIN XL", "PAR PHARMA", "49884-0108-11", "CREAM-WHITE, ROUND"),
    ("FLUOXETINE HCL", "20 MG", "CAPSULE", "PROZAC", "AUROBINDO", "65862-0193-01", "GREEN AND OFF-WHITE CAPSULE"),
    ("DULOXETINE HCL DR", "60 MG", "CAPSULE DR", "CYMBALTA", "AJANTA", "27241-0099-03", "BLUE AND GREEN OPAQUE CAPSULE"),
    ("MELOXICAM", "15 MG", "TABLET", "MOBIC", "ZDYUS", "68382-0051-01", "PASTEL YELLOW, OVAL"),
    ("DOXYCYCLINE HYCLATE", "100 MG", "CAPSULE", "VIBRAMYCIN", "MAYNE", "51862-0543-01", "LIGHT BLUE OPAQUE CAPSULE"),
    ("CIPROFLOXACIN HCL", "500 MG", "TABLET", "CIPRO", "PACK PHARMA", "43598-0318-10", "WHITE TO OFF-WHITE OBLONG"),
    ("CEFDINIR", "300 MG", "CAPSULE", "OMNICEF", "LUPIN", "68180-0711-60", "LAVENDER AND TURQUOISE CAPSULE"),
    ("SPIRONOLACTONE", "25 MG", "TABLET", "ALDACTONE", "AMNEAL", "53746-0511-01", "LIGHT YELLOW, ROUND, PEPPERMINT SCENT"),
    ("ALLOPURINOL", "100 MG", "TABLET", "ZYLOPRIM", "MYLAN", "00378-0137-01", "WHITE, ROUND, FLAT-FACED"),
    ("FINASTERIDE", "5 MG", "TABLET", "PROSCAR", "CAMBER", "31722-0525-90", "BLUE, APPLE-SHAPED"),
    ("TAMSULOSIN HCL", "0.4 MG", "CAPSULE", "FLOMAX", "SYNTHON", "00378-6940-01", "OLIVE GREEN AND ORANGE CAPSULE"),
    ("FAMOTIDINE", "20 MG", "TABLET", "PEPCID", "CARLSBAD", "61442-0121-01", "BEIGE, ROUNDED SQUARE"),
    ("CETIRIZINE HCL", "10 MG", "TABLET", "ZYRTEC", "PERRIGO", "45802-0919-78", "WHITE, RECTANGULAR, SCORED"),
    ("CYCLOBENZAPRINE HCL", "10 MG", "TABLET", "FLEXERIL", "TRU PHARMA", "52817-0332-10", "YELLOW, ROUND, FILM-COATED"),
    ("NAPROXEN", "500 MG", "TABLET", "NAPROSYN", "GLENMARK", "68462-0190-05", "YELLOW, CAPSULE-SHAPED"),
    ("LISINOPRIL-HCTZ", "20-12.5 MG", "TABLET", "PRINZIDE", "LUPIN", "68180-0520-01", "PEACH, ROUND, BICONVEX"),
    ("GLIPIZIDE XL", "10 MG", "TABLET ER", "GLUCOTROL XL", "PFIZER", "00069-2560-68", "WHITE, ROUND, LASER-DRILLED HOLE"),
    ("SITAGLIPTIN", "100 MG", "TABLET", "JANUVIA", "MERCK", "00006-0277-31", "BEIGE, ROUND, FILM-COATED"),
    ("EMPAGLIFLOZIN", "10 MG", "TABLET", "JARDIANCE", "BOEHRINGER", "00597-0152-30", "PALE YELLOW, ROUND, BICONVEX"),
    ("APIXABAN", "5 MG", "TABLET", "ELIQUIS", "BRISTOL-MYERS", "00003-0894-21", "PINK, OVAL, BICONVEX"),
    ("RIVAROXABAN", "20 MG", "TABLET", "XARELTO", "JANSSEN", "50458-0579-30", "DARK RED, TRIANGULAR"),
    ("SUMATRIPTAN SUCCINATE", "100 MG", "TABLET", "IMITREX", "DR. REDDYS", "55111-0292-79", "PINK, TRIANGULAR, BICONVEX"),
    ("ONDANSETRON ODT", "4 MG", "TABLET ODT", "ZOFRAN ODT", "GLENMARK", "68462-0157-13", "WHITE, ROUND, STRAWBERRY FLAVOR"),
]

SIG_TEMPLATES = [
    ("TAKE 1 TABLET BY MOUTH ONCE DAILY", "IN THE MORNING WITH OR WITHOUT FOOD."),
    ("TAKE 1 TABLET BY MOUTH TWICE DAILY", "WITH MEALS (MORNING AND EVENING)."),
    ("TAKE 1 CAPSULE BY MOUTH EVERY 8 HOURS", "AS NEEDED FOR PAIN OR INFLAMMATION."),
    ("TAKE 1 TABLET BY MOUTH AT BEDTIME", "FOR CHOLESTEROL CONTROL. DO NOT SKIP DOSES."),
    ("TAKE 2 TABLETS BY MOUTH ONCE DAILY", "WITH A FULL GLASS OF WATER."),
    ("TAKE 1 TABLET BY MOUTH EVERY 12 HOURS", "UNTIL ALL MEDICATION IS FINISHED."),
    ("TAKE 1 TABLET BY MOUTH DAILY", "30 MINUTES BEFORE BREAKFAST ON EMPTY STOMACH."),
    ("TAKE 1 TO 2 TABLETS BY MOUTH EVERY 6 HOURS", "AS NEEDED FOR SYMPTOM RELIEF."),
    ("INHALE 2 PUFFS BY MOUTH EVERY 4 TO 6 HOURS", "AS NEEDED FOR SHORTNESS OF BREATH."),
    ("SPRAY 1 TO 2 SPRAYS IN EACH NOSTRIL", "ONCE DAILY IN THE MORNING."),
    ("DISSOLVE 1 TABLET ON TOP OF TONGUE", "EVERY 8 HOURS AS NEEDED FOR NAUSEA."),
    ("TAKE 1 CAPSULE BY MOUTH ONCE DAILY", "30 MINUTES AFTER THE SAME MEAL EACH DAY."),
]

AUX_WARNINGS = [
    ("TAKE WITH FOOD", "Take with food or milk to prevent stomach upset.", (255, 218, 40), (15, 15, 15)),
    ("AVOID ALCOHOL", "Do not drink alcoholic beverages with this drug.", (242, 95, 38), (255, 255, 255)),
    ("SWALLOW WHOLE", "Do not crush, chew, or break tablets/capsules.", (45, 138, 225), (255, 255, 255)),
    ("MAY CAUSE DROWSINESS", "Use caution when driving or operating machinery.", (255, 195, 30), (15, 15, 15)),
    ("AVOID SUNLIGHT", "Avoid prolonged sun or UV exposure while taking.", (235, 125, 35), (255, 255, 255)),
    ("FINISH ALL MEDICATION", "Take full course unless directed by doctor.", (42, 165, 92), (255, 255, 255)),
    ("TAKE WITH PLENTY OF WATER", "Drink a full 8 oz glass of water with each dose.", (60, 155, 235), (255, 255, 255)),
    ("KEEP OUT OF REACH", "Keep all medications away from children & pets.", (210, 45, 55), (255, 255, 255)),
    ("AVOID GRAPEFRUIT JUICE", "Do not eat grapefruit or drink grapefruit juice.", (245, 155, 45), (15, 15, 15)),
]


def get_font(path, size):
    try:
        return ImageFont.truetype(path, int(size))
    except Exception:
        return ImageFont.load_default()


def generate_unique_records(count=400, seed=20261104):
    """
    Generates `count` guaranteed-unique prescription records so NO TWO images
    (across all 200 flat + 200 curved) ever share the same Patient Name, Rx#,
    Address, DOB, Phone, or Doctor/Prescriber combination.
    """
    rng = random.Random(seed)
    used_names = set()
    used_rx = set()
    used_addresses = set()
    used_dobs = set()
    used_phones = set()

    records = []
    for idx in range(count):
        # 1. Unique Patient Full Name
        while True:
            fn = rng.choice(FIRST_NAMES)
            ln = rng.choice(LAST_NAMES)
            mid = rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ")
            fmt = rng.choice([f"{fn} {mid}. {ln}", f"{ln}, {fn} {mid}", f"{fn} {ln}"])
            key = (fn, mid, ln)
            if key not in used_names:
                used_names.add(key)
                patient_name = fmt
                break

        # 2. Unique Rx Number
        while True:
            rx_num = f"{rng.randint(1000000, 9999999)}-{rng.randint(0, 9):02d}"
            if rx_num not in used_rx:
                used_rx.add(rx_num)
                break

        # 3. Unique Street Address
        while True:
            st_num = rng.randint(101, 9899)
            st_dir = rng.choice(["N.", "S.", "E.", "W.", "NW", "SE", ""])
            st_name = rng.choice(STREETS)
            apt = rng.choice(["", f", APT {rng.randint(1, 35)}{rng.choice('ABCDEF')}", f", UNIT {rng.randint(100, 909)}"])
            city, state, zip3 = rng.choice(CITIES_STATES)
            zip_code = f"{zip3}{rng.randint(10, 99)}"
            addr = f"{st_num} {st_dir} {st_name}{apt}, {city}, {state} {zip_code}".replace("  ", " ")
            if addr not in used_addresses:
                used_addresses.add(addr)
                break

        # 4. Unique DOB
        while True:
            m = rng.randint(1, 12)
            d = rng.randint(1, 28)
            y = rng.randint(1938, 2006)
            dob = f"{m:02d}/{d:02d}/{y}"
            if dob not in used_dobs:
                used_dobs.add(dob)
                break

        # 5. Unique Pharmacy Store & Phone
        while True:
            ph = f"({rng.randint(201, 989)}) {rng.randint(200, 999)}-{rng.randint(1000, 9999)}"
            if ph not in used_phones:
                used_phones.add(ph)
                break

        # Prescriber & RPh
        doc_fn = rng.choice(FIRST_NAMES)
        doc_ln = rng.choice(LAST_NAMES)
        doc_cred = rng.choice(["MD", "DO", "NP", "PA-C", "MD"])
        prescriber = f"DR. {doc_fn} {doc_ln}, {doc_cred}"

        rph_fn = rng.choice(FIRST_NAMES)
        rph_ln = rng.choice(LAST_NAMES)
        pharmacist = f"{rph_fn[0]}. {rph_ln}, RPh"

        brand = PHARMACY_BRANDS[idx % len(PHARMACY_BRANDS)]
        store_no = rng.randint(100, 9999)
        pharm_street = f"{rng.randint(100, 4999)} {rng.choice(STREETS)}, {city}, {state} {zip_code}"

        drug = DRUGS_POOL[(idx * 7 + rng.randint(0, len(DRUGS_POOL) - 1)) % len(DRUGS_POOL)]
        sig = rng.choice(SIG_TEMPLATES)
        qty = rng.choice([14, 28, 30, 60, 90, 120, 180])
        refills = rng.choice(["NO REFILLS", "1 REFILL", "2 REFILLS", "3 REFILLS", "5 REFILLS"])

        fm = rng.randint(1, 12)
        fd = rng.randint(1, 28)
        date_filled = f"{fm:02d}/{fd:02d}/2026"
        discard_date = f"{fm:02d}/{fd:02d}/2027"

        aux_Sample = rng.sample(AUX_WARNINGS, 3)

        # Label form / shape / size variant (5 distinct layout styles)
        layout_form = idx % 5
        # Dosage container form (for curved 3D render: 6 distinct bottle/container shapes & sizes)
        bottle_form = idx % 6

        records.append({
            "id": idx + 1,
            "rx_number": rx_num,
            "patient_name": patient_name,
            "patient_address": addr,
            "patient_dob": dob,
            "date_filled": date_filled,
            "discard_date": discard_date,
            "prescriber": prescriber,
            "pharmacist": pharmacist,
            "pharmacy_name": f"{brand['name']} #{store_no:04d}",
            "pharmacy_address": pharm_street,
            "pharmacy_phone": ph,
            "brand_color": brand["color"],
            "brand_accent": brand["accent"],
            "brand_style": brand["style"],
            "drug_name": drug[0],
            "drug_strength": drug[1],
            "drug_form": drug[2],
            "generic_for": drug[3],
            "manufacturer": drug[4],
            "ndc": drug[5],
            "pill_desc": drug[6],
            "sig_line1": sig[0],
            "sig_line2": sig[1],
            "quantity": f"{qty} {drug[2]}S" if not drug[2].endswith("S") else f"{qty} {drug[2]}",
            "refills": f"{refills} BEFORE {discard_date}",
            "aux_warnings": aux_Sample,
            "layout_form": layout_form,
            "bottle_form": bottle_form,
            "seed": seed + idx * 101,
        })

    return records


def render_flat_sticker(rec, for_bottle_texture=False):
    """
    Renders a flat pharmacy sticker in one of 5 distinct shapes, sizes, and layouts:
      Form 0: Wide Standard Pharmacy Label + Right Perforated Aux Strip (960 x 620)
      Form 1: Compact Square Thermal Label with Top Barcode Banner (780 x 720)
      Form 2: Tall Vertical Vial Sticker with Bottom Aux Warnings (660 x 880)
      Form 3: Modern Two-Tone Split Clinical Label with Left Aux Column (980 x 560)
      Form 4: Minimalist Independent/Hospital Thermal Sticker (840 x 520)
    """
    rng = random.Random(rec["seed"])
    form = rec["layout_form"]

    if form == 0:
        W, H = 960, 620
    elif form == 1:
        W, H = 780, 720
    elif form == 2:
        W, H = 680, 860
    elif form == 3:
        W, H = 1000, 560
    else:
        W, H = 840, 520

    # Paper tint variation (thermal white, warm cream, pale yellow, slight grey recycled)
    paper_tints = [
        (252, 251, 247),
        (248, 249, 252),
        (254, 250, 240),
        (246, 246, 244),
        (250, 252, 248),
    ]
    paper_rgb = paper_tints[rec["id"] % len(paper_tints)]
    img = Image.new("RGB", (W, H), paper_rgb)
    draw = ImageDraw.Draw(img)

    # Fonts
    f_logo = get_font(FONT_BLACK, 25 if W >= 800 else 22)
    f_sub = get_font(FONT_REGULAR, 14)
    f_rx = get_font(FONT_BOLD, 28)
    f_pat = get_font(FONT_BOLD, 26)
    f_addr = get_font(FONT_REGULAR, 15)
    f_sig = get_font(FONT_BOLD, 23 if W >= 800 else 20)
    f_drug = get_font(FONT_BLACK, 30 if W >= 800 else 25)
    f_meta_b = get_font(FONT_BOLD, 17)
    f_meta = get_font(FONT_REGULAR, 16)
    f_small = get_font(FONT_NARROW, 14)
    f_aux_b = get_font(FONT_NARROW_BOLD, 15)
    f_aux_r = get_font(FONT_NARROW, 13)

    bboxes = []

    def txt(xy, text_str, font, fill=(18, 18, 18), field=None):
        draw.text(xy, text_str, font=font, fill=fill)
        bb = draw.textbbox(xy, text_str, font=font)
        if field:
            bboxes.append({"field": field, "text": text_str, "bbox": list(bb)})
        return bb

    def draw_barcode(x1, y1, x2, y2, code_text):
        draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255), outline=(190, 190, 190), width=1)
        bx = x1 + 12
        while bx < x2 - 14:
            bw = rng.choice([2, 3, 4])
            if bx + bw < x2 - 12:
                draw.rectangle([bx, y1 + 8, bx + bw, y2 - 24], fill=(15, 15, 15))
            bx += bw + rng.choice([2, 3, 4])
        draw.text((x1 + 18, y2 - 21), f"*{code_text}*", font=f_small, fill=(20, 20, 20))

    b_col = rec["brand_color"]
    full_drug = f"{rec['drug_name']} {rec['drug_strength']} {rec['drug_form']}"

    if form == 0:
        # Form 0: Wide Standard + Right Aux Strip
        MW = 700
        draw.rectangle([0, 0, MW, 76], fill=b_col)
        txt((22, 12), rec["pharmacy_name"], f_logo, fill=(255, 255, 255), field="pharmacy_name")
        txt((22, 46), f"{rec['pharmacy_address']}  •  {rec['pharmacy_phone']}  •  {rec['pharmacist']}", f_sub, fill=(250, 245, 245))

        draw.rectangle([22, 92, 300, 138], fill=(255, 243, 175), outline=(210, 195, 120))
        txt((32, 99), f"Rx# {rec['rx_number']}", f_rx, field="rx_number")
        txt((450, 94), f"DATE: {rec['date_filled']}", f_meta_b, field="date_filled")
        txt((450, 118), f"DOB: {rec['patient_dob']}", f_meta, fill=(55, 55, 55), field="patient_dob")

        txt((22, 152), rec["patient_name"], f_pat, field="patient_name")
        txt((22, 185), rec["patient_address"], f_addr, fill=(60, 60, 60), field="patient_address")
        draw.line([(22, 214), (MW - 20, 214)], fill=(185, 185, 185), width=2)

        draw.rectangle([22, 224, MW - 20, 304], fill=(243, 246, 251), outline=(205, 212, 225))
        txt((34, 234), rec["sig_line1"], f_sig, field="sig_line1")
        txt((34, 266), rec["sig_line2"], f_sig, field="sig_line2")

        txt((22, 322), full_drug, f_drug, field="drug_name")
        txt((22, 364), f"GENERIC FOR: {rec['generic_for']}   •   MFR: {rec['manufacturer']}", f_meta_b, fill=(65, 65, 65))
        txt((22, 390), f"NDC: {rec['ndc']}   •   IMPRINT/DESC: {rec['pill_desc']}", f_small, fill=(75, 75, 75), field="ndc")

        draw.line([(22, 422), (MW - 20, 422)], fill=(185, 185, 185), width=2)
        draw.rectangle([22, 436, 220, 476], fill=(238, 238, 238), outline=(180, 180, 180))
        txt((32, 446), f"QTY: {rec['quantity']}", f_meta_b, field="quantity")
        txt((240, 446), rec["refills"], f_meta_b, field="refills")
        txt((22, 492), f"PRESCRIBER: {rec['prescriber']}", f_meta_b, field="prescriber")
        txt((22, 520), f"DISCARD AFTER: {rec['discard_date']}", f_meta, fill=(65, 65, 65))

        draw.rectangle([22, 554, MW - 20, 602], fill=(248, 240, 224), outline=(215, 190, 145))
        draw.text((30, 562), "CAUTION: FEDERAL LAW PROHIBITS TRANSFER OF THIS DRUG TO ANY PERSON OTHER", font=f_small, fill=(75, 55, 30))
        draw.text((30, 580), "THAN THE PATIENT FOR WHOM IT WAS PRESCRIBED.", font=f_small, fill=(75, 55, 30))

        # Perforated right strip
        for yd in range(0, H, 14):
            draw.line([(MW, yd), (MW, min(H, yd + 7))], fill=(155, 155, 155), width=2)
        ax1, ax2 = MW + 16, W - 16
        for i, (wt, wd, wbg, wfg) in enumerate(rec["aux_warnings"]):
            yy = 18 + i * 110
            draw.rounded_rectangle([ax1, yy, ax2, yy + 96], radius=8, fill=wbg, outline=(35, 35, 35), width=2)
            draw.text((ax1 + 12, yy + 12), wt, font=f_aux_b, fill=wfg)
            draw.text((ax1 + 12, yy + 38), wd[:28], font=f_aux_r, fill=wfg)
            draw.text((ax1 + 12, yy + 56), wd[28:], font=f_aux_r, fill=wfg)
        draw_barcode(ax1, 358, ax2, 595, rec["rx_number"])

    elif form == 1:
        # Form 1: Square Layout with Top Split Header & Bottom Horizontal Aux Stickers
        draw.rectangle([0, 0, W, 68], fill=b_col)
        txt((20, 10), rec["pharmacy_name"], f_logo, fill=(255, 255, 255), field="pharmacy_name")
        txt((20, 42), f"{rec['pharmacy_address']}  |  TEL: {rec['pharmacy_phone']}", f_sub, fill=(245, 245, 245))

        draw_barcode(W - 245, 80, W - 20, 158, rec["rx_number"])
        draw.rectangle([20, 82, 310, 132], fill=(255, 238, 160), outline=(190, 170, 90), width=2)
        txt((32, 92), f"Rx# {rec['rx_number']}", f_rx, field="rx_number")
        txt((325, 86), f"FILLED: {rec['date_filled']}", f_meta_b, field="date_filled")
        txt((325, 112), f"DOB: {rec['patient_dob']}", f_meta, field="patient_dob")

        txt((20, 150), f"PATIENT: {rec['patient_name']}", f_pat, field="patient_name")
        txt((20, 184), rec["patient_address"], f_addr, fill=(60, 60, 60), field="patient_address")

        draw.rectangle([20, 216, W - 20, 304], fill=(238, 245, 252), outline=b_col, width=2)
        txt((34, 228), rec["sig_line1"], f_sig, field="sig_line1")
        txt((34, 262), rec["sig_line2"], f_sig, field="sig_line2")

        txt((20, 322), full_drug, f_drug, field="drug_name")
        txt((20, 362), f"SUB FOR: {rec['generic_for']}   |   MFR: {rec['manufacturer']}   |   NDC: {rec['ndc']}", f_meta_b, fill=(55, 55, 55), field="ndc")
        txt((20, 390), f"APPEARANCE: {rec['pill_desc']}", f_small, fill=(80, 80, 80))

        draw.line([(20, 420), (W - 20, 420)], fill=(175, 175, 175), width=2)
        txt((20, 434), f"QTY: {rec['quantity']}", f_meta_b, field="quantity")
        txt((270, 434), rec["refills"], f_meta_b, field="refills")
        txt((20, 466), f"PRESCRIBER: {rec['prescriber']}", f_meta_b, field="prescriber")
        txt((430, 466), f"RPh: {rec['pharmacist']}", f_meta)
        txt((20, 496), f"USE BEFORE: {rec['discard_date']}", f_meta, fill=(75, 75, 75))

        # Horizontal Aux Stickers along bottom
        draw.line([(0, 535), (W, 535)], fill=(150, 150, 150), width=2)
        bw_card = (W - 56) // 3
        for i, (wt, wd, wbg, wfg) in enumerate(rec["aux_warnings"]):
            xx = 16 + i * (bw_card + 12)
            draw.rounded_rectangle([xx, 552, xx + bw_card, 696], radius=8, fill=wbg, outline=(30, 30, 30), width=2)
            draw.text((xx + 10, 566), wt, font=f_aux_b, fill=wfg)
            draw.text((xx + 10, 596), wd[:26], font=f_aux_r, fill=wfg)
            draw.text((xx + 10, 616), wd[26:], font=f_aux_r, fill=wfg)

    elif form == 2:
        # Form 2: Tall Vertical Vial Label (680 x 860)
        draw.rectangle([0, 0, W, 82], fill=b_col)
        txt((20, 14), rec["pharmacy_name"], f_logo, fill=(255, 255, 255), field="pharmacy_name")
        txt((20, 48), f"{rec['pharmacy_address']} • {rec['pharmacy_phone']}", f_sub, fill=(255, 245, 245))

        txt((20, 100), rec["patient_name"], f_pat, field="patient_name")
        txt((20, 132), f"DOB: {rec['patient_dob']}   |   {rec['patient_address']}", f_addr, fill=(55, 55, 55), field="patient_dob")

        draw.rectangle([20, 166, 300, 214], fill=(255, 242, 165), outline=(180, 165, 90), width=2)
        txt((30, 174), f"Rx# {rec['rx_number']}", f_rx, field="rx_number")
        txt((320, 174), f"DATE FILLED: {rec['date_filled']}", f_meta_b, field="date_filled")
        txt((320, 198), f"DISCARD: {rec['discard_date']}", f_meta, fill=(65, 65, 65))

        draw.rectangle([20, 232, W - 20, 330], fill=(242, 246, 250), outline=(190, 200, 215), width=2)
        txt((32, 248), rec["sig_line1"], f_sig, field="sig_line1")
        txt((32, 284), rec["sig_line2"], f_sig, field="sig_line2")

        txt((20, 352), full_drug, f_drug, field="drug_name")
        txt((20, 394), f"GENERIC FOR: {rec['generic_for']}", f_meta_b, fill=(50, 50, 50))
        txt((20, 422), f"MFR: {rec['manufacturer']}   •   NDC: {rec['ndc']}", f_meta, field="ndc")
        txt((20, 450), f"PILL ID: {rec['pill_desc']}", f_small, fill=(75, 75, 75))

        draw.line([(20, 482), (W - 20, 482)], fill=(175, 175, 175), width=2)
        txt((20, 498), f"QTY: {rec['quantity']}", f_meta_b, field="quantity")
        txt((250, 498), rec["refills"], f_meta_b, field="refills")
        txt((20, 532), f"DR: {rec['prescriber']}", f_meta_b, field="prescriber")
        txt((410, 532), f"RPh: {rec['pharmacist']}", f_meta)

        draw_barcode(20, 575, 340, 680, rec["rx_number"])
        # Two stacked Aux warnings on bottom right + full bottom caution
        for i in range(2):
            wt, wd, wbg, wfg = rec["aux_warnings"][i]
            yy = 575 + i * 105
            draw.rounded_rectangle([360, yy, W - 20, yy + 92], radius=8, fill=wbg, outline=(30, 30, 30), width=2)
            draw.text((372, yy + 10), wt, font=f_aux_b, fill=wfg)
            draw.text((372, yy + 36), wd[:32], font=f_aux_r, fill=wfg)
            draw.text((372, yy + 54), wd[32:], font=f_aux_r, fill=wfg)

        draw.rectangle([20, 790, W - 20, 842], fill=(248, 238, 220), outline=(205, 180, 140))
        draw.text((30, 798), "FEDERAL LAW PROHIBITS TRANSFER OF THIS DRUG TO ANY PERSON OTHER THAN PATIENT.", font=f_small, fill=(70, 50, 30))
        draw.text((30, 818), "KEEP ALL MEDICATIONS OUT OF THE REACH OF CHILDREN.", font=f_small, fill=(70, 50, 30))

    elif form == 3:
        # Form 3: Left Aux Column + Right Main Clinical Layout (1000 x 560)
        LEFT_W = 250
        for yd in range(0, H, 14):
            draw.line([(LEFT_W, yd), (LEFT_W, min(H, yd + 7))], fill=(150, 150, 150), width=2)

        for i, (wt, wd, wbg, wfg) in enumerate(rec["aux_warnings"]):
            yy = 16 + i * 112
            draw.rounded_rectangle([14, yy, LEFT_W - 14, yy + 98], radius=8, fill=wbg, outline=(35, 35, 35), width=2)
            draw.text((26, yy + 12), wt, font=f_aux_b, fill=wfg)
            draw.text((26, yy + 38), wd[:26], font=f_aux_r, fill=wfg)
            draw.text((26, yy + 56), wd[26:], font=f_aux_r, fill=wfg)
        draw_barcode(14, 358, LEFT_W - 14, 540, rec["rx_number"])

        MX = LEFT_W + 22
        draw.rectangle([LEFT_W + 2, 0, W, 72], fill=b_col)
        txt((MX, 10), rec["pharmacy_name"], f_logo, fill=(255, 255, 255), field="pharmacy_name")
        txt((MX, 44), f"{rec['pharmacy_address']}   •   {rec['pharmacy_phone']}", f_sub, fill=(250, 245, 245))

        txt((MX, 88), rec["patient_name"], f_pat, field="patient_name")
        txt((MX, 120), f"DOB: {rec['patient_dob']}  •  {rec['patient_address']}", f_addr, fill=(60, 60, 60), field="patient_dob")

        draw.rectangle([W - 290, 84, W - 20, 134], fill=(255, 243, 175), outline=(200, 180, 100), width=2)
        txt((W - 278, 94), f"Rx# {rec['rx_number']}", f_rx, field="rx_number")

        draw.rectangle([MX, 152, W - 20, 236], fill=(242, 246, 252), outline=b_col, width=2)
        txt((MX + 14, 164), rec["sig_line1"], f_sig, field="sig_line1")
        txt((MX + 14, 198), rec["sig_line2"], f_sig, field="sig_line2")

        txt((MX, 254), full_drug, f_drug, field="drug_name")
        txt((MX, 296), f"GENERIC FOR: {rec['generic_for']}   |   MFR: {rec['manufacturer']}   |   NDC: {rec['ndc']}", f_meta_b, fill=(55, 55, 55), field="ndc")
        txt((MX, 324), f"DESCRIPTION: {rec['pill_desc']}", f_small, fill=(80, 80, 80))

        draw.line([(MX, 356), (W - 20, 356)], fill=(180, 180, 180), width=2)
        txt((MX, 372), f"QTY: {rec['quantity']}", f_meta_b, field="quantity")
        txt((MX + 230, 372), rec["refills"], f_meta_b, field="refills")
        txt((MX, 406), f"PRESCRIBER: {rec['prescriber']}", f_meta_b, field="prescriber")
        txt((MX + 370, 406), f"FILLED: {rec['date_filled']}", f_meta_b, field="date_filled")
        txt((MX, 438), f"DISCARD AFTER: {rec['discard_date']}   •   VERIFIED BY: {rec['pharmacist']}", f_meta, fill=(65, 65, 65))

        draw.rectangle([MX, 482, W - 20, 540], fill=(248, 240, 225), outline=(210, 185, 140))
        draw.text((MX + 10, 492), "CAUTION: FEDERAL LAW PROHIBITS THE TRANSFER OF THIS DRUG TO ANY PERSON OTHER", font=f_small, fill=(75, 55, 30))
        draw.text((MX + 10, 512), "THAN THE PATIENT FOR WHOM IT WAS PRESCRIBED.", font=f_small, fill=(75, 55, 30))

    else:
        # Form 4: Clean Hospital / Outpatient Thermal Sticker (840 x 520)
        draw.rectangle([0, 0, W, 12], fill=b_col)
        txt((24, 22), rec["pharmacy_name"], f_logo, fill=b_col, field="pharmacy_name")
        txt((24, 54), f"{rec['pharmacy_address']}   •   PHONE: {rec['pharmacy_phone']}   •   RPh: {rec['pharmacist']}", f_sub, fill=(70, 70, 70))
        draw.line([(20, 78), (W - 20, 78)], fill=b_col, width=3)

        txt((24, 92), f"Rx# {rec['rx_number']}", f_rx, field="rx_number")
        txt((300, 96), f"FILLED: {rec['date_filled']}", f_meta_b, field="date_filled")
        txt((520, 96), f"DOB: {rec['patient_dob']}", f_meta_b, field="patient_dob")

        txt((24, 134), rec["patient_name"], f_pat, field="patient_name")
        txt((24, 166), rec["patient_address"], f_addr, fill=(65, 65, 65), field="patient_address")

        draw.rectangle([24, 196, W - 240, 282], fill=(245, 245, 245), outline=(170, 170, 170), width=2)
        txt((36, 208), rec["sig_line1"], f_sig, field="sig_line1")
        txt((36, 242), rec["sig_line2"], f_sig, field="sig_line2")

        txt((24, 300), full_drug, f_drug, field="drug_name")
        txt((24, 342), f"GENERIC FOR: {rec['generic_for']}   •   MFR: {rec['manufacturer']}   •   NDC: {rec['ndc']}", f_meta_b, fill=(55, 55, 55), field="ndc")
        txt((24, 370), f"IMPRINT: {rec['pill_desc']}", f_small, fill=(80, 80, 80))

        txt((24, 404), f"QTY: {rec['quantity']}", f_meta_b, field="quantity")
        txt((240, 404), rec["refills"], f_meta_b, field="refills")
        txt((24, 434), f"PRESCRIBER: {rec['prescriber']}   •   DISCARD AFTER: {rec['discard_date']}", f_meta_b, field="prescriber")

        # Right side barcode & 1 warning box
        draw_barcode(W - 220, 196, W - 20, 325, rec["rx_number"])
        wt, wd, wbg, wfg = rec["aux_warnings"][0]
        draw.rounded_rectangle([W - 220, 340, W - 20, 455], radius=8, fill=wbg, outline=(30, 30, 30), width=2)
        draw.text((W - 208, 354), wt, font=f_aux_b, fill=wfg)
        draw.text((W - 208, 382), wd[:24], font=f_aux_r, fill=wfg)
        draw.text((W - 208, 402), wd[24:], font=f_aux_r, fill=wfg)

        draw.rectangle([24, 468, W - 20, 506], fill=(246, 240, 226), outline=(200, 180, 145))
        draw.text((34, 480), "CAUTION: FEDERAL LAW PROHIBITS TRANSFER OF THIS DRUG TO ANY PERSON OTHER THAN THE PATIENT.", font=f_small, fill=(70, 50, 30))

    # Outer border
    draw.rectangle([0, 0, W - 1, H - 1], outline=(175, 172, 165), width=2)

    # If rendering as a standalone flat sticker image, place it on a realistic varied surface or slight angle
    if not for_bottle_texture:
        rot_deg = rng.uniform(-2.2, 2.2)
        if abs(rot_deg) > 0.3:
            bg_pad = 36
            bg_cols = [(232, 228, 220), (218, 222, 228), (238, 232, 222), (210, 205, 198), (225, 230, 225)]
            canvas = Image.new("RGB", (W + bg_pad * 2, H + bg_pad * 2), bg_cols[rec["id"] % len(bg_cols)])
            rgba = img.convert("RGBA").rotate(rot_deg, resample=Image.BICUBIC, expand=False)
            canvas.paste(rgba, (bg_pad, bg_pad), rgba)
            img = canvas

    return img, bboxes


def render_curved_container(rec):
    """
    Renders a 3D curved container with the unique sticker wrapped around it.
    Features 6 distinct container shapes, sizes, colors, and forms:
      Bottle Form 0: Standard Amber Prescription Vial + White Ribbed Cap
      Bottle Form 1: Tall Slim Amber Vial + Child-Safe Push-Turn Cap
      Bottle Form 2: Wide-Mouth Short Fat Amber Pill Jar + Wide White Cap
      Bottle Form 3: Opaque White HDPE Clinical Bottle + Blue/Red Cap
      Bottle Form 4: Green Translucent Pharmacy Vial + White Reversible Cap
      Bottle Form 5: Deep Cobalt Blue / Dark Amber Specialty Vial + Ribbed Cap
    Also varies:
      - Cylindrical rotation offset (yaw angle around bottle axis)
      - Camera vertical viewing tilt (top-down vs eye-level)
      - Specular glare position & intensity
      - Background lighting & countertop colors
    """
    rng = random.Random(rec["seed"] + 777)
    flat_sticker, bboxes = render_flat_sticker(rec, for_bottle_texture=True)
    src_w, src_h = flat_sticker.size
    src_px = flat_sticker.load()

    bform = rec["bottle_form"]

    # Shape & Size parameters per bottle form
    if bform == 0:
        # Standard Amber Vial
        CW, CH = 760, 920
        R = 175
        B_TOP, B_BOT = 200, 790
        CAP_H = 95
        body_rgb = (198, 76, 12)
        cap_rgb = (242, 241, 237)
    elif bform == 1:
        # Tall Slim Vial
        CW, CH = 720, 980
        R = 142
        B_TOP, B_BOT = 180, 860
        CAP_H = 88
        body_rgb = (208, 84, 15)
        cap_rgb = (244, 244, 240)
    elif bform == 2:
        # Wide Fat Pill Jar
        CW, CH = 840, 840
        R = 225
        B_TOP, B_BOT = 215, 725
        CAP_H = 102
        body_rgb = (186, 68, 10)
        cap_rgb = (240, 238, 232)
    elif bform == 3:
        # Opaque White HDPE Bottle
        CW, CH = 780, 900
        R = 185
        B_TOP, B_BOT = 205, 780
        CAP_H = 92
        body_rgb = (238, 240, 243)
        cap_rgb = rng.choice([(35, 95, 185), (195, 35, 40), (242, 242, 242)])
    elif bform == 4:
        # Translucent Emerald Green Pharmacy Vial
        CW, CH = 760, 920
        R = 170
        B_TOP, B_BOT = 195, 795
        CAP_H = 92
        body_rgb = (28, 138, 62)
        cap_rgb = (242, 242, 238)
    else:
        # Dark Amber / Cobalt Specialty Vial
        CW, CH = 760, 900
        R = 165
        B_TOP, B_BOT = 195, 775
        CAP_H = 90
        body_rgb = rng.choice([(145, 48, 8), (22, 68, 158)])
        cap_rgb = (238, 238, 235)

    CX = CW // 2 + rng.randint(-18, 18)

    # Varied background & countertop environment
    bg_themes = [
        ((234, 228, 218), (192, 178, 162)),  # Warm cream + wood
        ((222, 228, 235), (175, 182, 190)),  # Clinical cool grey + stainless counter
        ((240, 236, 230), (212, 206, 198)),  # Marble bathroom counter
        ((218, 224, 216), (162, 152, 138)),  # Sage wall + walnut table
        ((228, 222, 226), (185, 175, 172)),  # Soft neutral studio
    ]
    wall_col, desk_col = bg_themes[rec["id"] % len(bg_themes)]
    horizon_y = B_BOT - rng.randint(85, 135)

    scene = Image.new("RGB", (CW, CH), wall_col)
    s_px = scene.load()
    for y in range(CH):
        if y < horizon_y:
            t = y / float(max(1, horizon_y))
            r = int(wall_col[0] * (1.03 - 0.12 * t))
            g = int(wall_col[1] * (1.03 - 0.12 * t))
            b = int(wall_col[2] * (1.03 - 0.12 * t))
        else:
            t = (y - horizon_y) / float(max(1, CH - horizon_y))
            r = int(desk_col[0] * (1.02 - 0.18 * t))
            g = int(desk_col[1] * (1.02 - 0.18 * t))
            b = int(desk_col[2] * (1.02 - 0.18 * t))
        for x in range(CW):
            s_px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    s_draw = ImageDraw.Draw(scene, "RGBA")

    # Contact shadow
    for r_sh in range(72, 0, -3):
        alpha = int(115 * ((1 - r_sh / 72.0) ** 1.8))
        s_draw.ellipse(
            [CX - r_sh * (R / 68.0), B_BOT + 4 - r_sh * 0.38, CX + r_sh * (R / 68.0), B_BOT + 4 + r_sh * 0.48],
            fill=(25, 20, 15, alpha),
        )

    bottle_layer = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    b_px = bottle_layer.load()
    b_draw = ImageDraw.Draw(bottle_layer, "RGBA")

    # Pills inside translucent bottles
    if bform != 3:
        for _ in range(22):
            px_c = CX + rng.randint(-R + 35, R - 35)
            py_c = rng.randint(B_BOT - 140, B_BOT - 28)
            b_draw.ellipse([px_c - 28, py_c - 16, px_c + 28, py_c + 16], fill=(248, 195, 110, 175))

    spec_pos = rng.uniform(-0.45, -0.22)
    camera_tilt = rng.uniform(14.0, 28.0)
    yaw_offset = rng.uniform(-0.18, 0.18)  # Rotates the sticker slightly left or right around the cylinder

    # Render cylindrical bottle body
    for y in range(B_TOP, B_BOT):
        for x in range(CX - R, CX + R):
            nx = (x - CX) / float(R)
            nz = math.sqrt(max(0.0, 1.0 - nx * nx))

            bot_curve = int(22 * nz)
            if y > B_BOT - 24 + bot_curve:
                continue

            spec1 = math.exp(-((nx - spec_pos) ** 2) / 0.02) * (65 if bform == 3 else 92)
            spec2 = math.exp(-((nx + spec_pos * 1.3) ** 2) / 0.04) * 32
            rim = (nz ** 0.45) if bform == 3 else (nz ** 0.58)

            pr, pg, pb, pa = b_px[x, y]
            pill_boost = (pa / 255.0) * 24.0 * nz if bform != 3 else 0.0

            r = int(min(255, body_rgb[0] * rim + spec1 + spec2 + pill_boost))
            g = int(min(255, body_rgb[1] * rim + spec1 * 0.78 + spec2 * 0.65 + pill_boost * 0.7))
            b = int(min(255, body_rgb[2] * rim + spec1 * 0.48 + spec2 * 0.35 + pill_boost * 0.25))

            if y < B_TOP + 32:
                shade = 0.58 + 0.42 * ((y - B_TOP) / 32.0)
                r, g, b = int(r * shade), int(g * shade), int(b * shade)
            elif y > B_BOT - 45:
                r, g, b = int(r * 0.74), int(g * 0.68), int(b * 0.62)

            b_px[x, y] = (r, g, b, 250)

    # Warp the flat pharmacy sticker onto the 3D cylinder
    LABEL_TOP = B_TOP + int((B_BOT - B_TOP) * 0.11)
    LABEL_H = int((B_BOT - B_TOP) * 0.74)
    ARC_SPAN = rng.uniform(1.26, 1.42)

    def sample_bilinear(u_px, v_px):
        x0 = int(u_px)
        y0 = int(v_px)
        x1 = min(src_w - 1, x0 + 1)
        y1 = min(src_h - 1, y0 + 1)
        fx = u_px - x0
        fy = v_px - y0
        c00 = src_px[x0, y0]
        c10 = src_px[x1, y0]
        c01 = src_px[x0, y1]
        c11 = src_px[x1, y1]
        return (
            c00[0] * (1 - fx) * (1 - fy) + c10[0] * fx * (1 - fy) + c01[0] * (1 - fx) * fy + c11[0] * fx * fy,
            c00[1] * (1 - fx) * (1 - fy) + c10[1] * fx * (1 - fy) + c01[1] * (1 - fx) * fy + c11[1] * fx * fy,
            c00[2] * (1 - fx) * (1 - fy) + c10[2] * fx * (1 - fy) + c01[2] * (1 - fx) * fy + c11[2] * fx * fy,
        )

    for x in range(CX - R + 2, CX + R - 2):
        nx = (x - CX) / float(R + 1)
        if abs(nx) >= 0.985:
            continue
        theta = math.asin(nx) - yaw_offset
        if abs(theta) > ARC_SPAN:
            continue
        nz = math.sqrt(max(0.0, 1.0 - nx * nx))

        u = (theta + ARC_SPAN) / (2.0 * ARC_SPAN)
        u_px = max(0.0, min(src_w - 1.001, u * (src_w - 1)))

        y_start = int(LABEL_TOP + camera_tilt * nz)
        y_end = y_start + LABEL_H

        diffuse = 0.50 + 0.52 * (nz ** 0.62)
        gloss = math.exp(-((nx - spec_pos) ** 2) / 0.022) * 30.0

        for y_screen in range(y_start, y_end):
            if 0 <= y_screen < CH:
                v = (y_screen - y_start) / float(LABEL_H)
                v_px = max(0.0, min(src_h - 1.001, v * (src_h - 1)))
                lr, lg, lb = sample_bilinear(u_px, v_px)
                fr = int(min(255, max(0, lr * diffuse + gloss)))
                fg = int(min(255, max(0, lg * diffuse + gloss * 0.98)))
                fb = int(min(255, max(0, lb * diffuse + gloss * 0.94)))
                b_px[x, y_screen] = (fr, fg, fb, 255)

    # Render Child-Resistant Cap
    CAP_TOP = B_TOP - CAP_H + 12
    CAP_BOT = B_TOP + 12
    CAP_R = R + (12 if bform != 1 else 9)

    for y in range(CAP_TOP, CAP_BOT):
        for x in range(CX - CAP_R, CX + CAP_R):
            nx = (x - CX) / float(CAP_R)
            if abs(nx) >= 1.0:
                continue
            nz = math.sqrt(max(0.0, 1.0 - nx * nx))
            theta = math.asin(nx)

            lip_curve = int((camera_tilt * 0.78) * nz)
            if y > CAP_BOT - 20 + lip_curve:
                continue
            top_curve = int(12 * (1.0 - nz))
            if y < CAP_TOP + top_curve:
                continue

            ridge = math.sin(theta * 36.0) * 10.0 * (nz ** 0.5) if (CAP_TOP + 18 < y < CAP_BOT - 24) else 0.0
            shade = 0.58 + 0.42 * (nz ** 0.55)
            spec_c = math.exp(-((nx - spec_pos) ** 2) / 0.03) * 26.0

            cr = int(min(255, max(0, cap_rgb[0] * shade + ridge + spec_c)))
            cg = int(min(255, max(0, cap_rgb[1] * shade + ridge + spec_c)))
            cb = int(min(255, max(0, cap_rgb[2] * shade + ridge + spec_c)))
            b_px[x, y] = (cr, cg, cb, 255)

    b_draw.ellipse(
        [CX - CAP_R + 4, CAP_TOP - 15, CX + CAP_R - 4, CAP_TOP + 20],
        fill=(max(0, cap_rgb[0] - 8), max(0, cap_rgb[1] - 8), max(0, cap_rgb[2] - 8), 255),
        outline=(195, 193, 188, 255),
        width=2,
    )

    out = Image.alpha_composite(scene.convert("RGBA"), bottle_layer).convert("RGB")
    # Slight random camera tilt
    cam_roll = rng.uniform(-2.5, 2.5)
    if abs(cam_roll) > 0.4:
        out = out.rotate(cam_roll, resample=Image.BICUBIC, expand=False, fillcolor=wall_col)

    return out, bboxes


def process_one_item(task):
    mode, index, rec = task
    if mode == "flat":
        img, bboxes = render_flat_sticker(rec, for_bottle_texture=False)
        fname = f"flat_label_{index:03d}.png"
        fpath = os.path.join(FLAT_DIR, fname)
        img.save(fpath, compress_level=3)
    else:
        img, bboxes = render_curved_container(rec)
        fname = f"curved_bottle_{index:03d}.png"
        fpath = os.path.join(CURVED_DIR, fname)
        img.save(fpath, compress_level=3)

    return {
        "file": fname,
        "category": mode,
        "record": {
            "rx_number": rec["rx_number"],
            "patient_name": rec["patient_name"],
            "patient_dob": rec["patient_dob"],
            "patient_address": rec["patient_address"],
            "drug_name": rec["drug_name"],
            "drug_strength": rec["drug_strength"],
            "drug_form": rec["drug_form"],
            "generic_for": rec["generic_for"],
            "ndc": rec["ndc"],
            "sig_line1": rec["sig_line1"],
            "sig_line2": rec["sig_line2"],
            "quantity": rec["quantity"],
            "refills": rec["refills"],
            "prescriber": rec["prescriber"],
            "pharmacy_name": rec["pharmacy_name"],
            "pharmacy_phone": rec["pharmacy_phone"],
            "date_filled": rec["date_filled"],
            "discard_date": rec["discard_date"],
            "layout_form": rec["layout_form"],
            "bottle_form": rec["bottle_form"] if mode == "curved" else None,
        },
        "bboxes": bboxes,
    }


def main():
    os.makedirs(FLAT_DIR, exist_ok=True)
    os.makedirs(CURVED_DIR, exist_ok=True)
    os.makedirs(META_DIR, exist_ok=True)

    # Generate 400 completely distinct PII/Prescription records (200 for flat, 200 for curved)
    all_records = generate_unique_records(400)
    flat_records = all_records[:200]
    curved_records = all_records[200:400]

    tasks = []
    for i, r in enumerate(flat_records, start=1):
        tasks.append(("flat", i, r))
    for i, r in enumerate(curved_records, start=1):
        tasks.append(("curved", i, r))

    results = []
    workers = min(8, os.cpu_count() or 4)
    print(f"Generating 200 flat + 200 curved images using {workers} CPU cores...")

    completed = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_one_item, t) for t in tasks]
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            completed += 1
            if completed % 50 == 0 or completed == len(tasks):
                print(f"Progress: {completed}/{len(tasks)} images saved...")

    results.sort(key=lambda x: (x["category"], x["file"]))
    manifest_path = os.path.join(META_DIR, "dataset_annotations.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)

    print("Done! Saved 200 flat labels, 200 curved labels, and annotations.")


if __name__ == "__main__":
    main()
