'''Split text to sentences.

Original idea from Perl's Lingua::EN::Sentence, modifications by Raymond
Hettinger.
'''

PEOPLE = [
    'jr', 'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'sen' 'sens', 'rep', 'reps',
    'gov', 'atty', 'attys', 'supt', 'det', 'rev',
]

ARMY = [
    'col', 'gen', 'lt', 'cmdr', 'adm', 'capt', 'sgt', 'cpl', 'maj',
]

INSTITUTES = [
    'dept', 'univ', 'assn', 'bros',
]

COMPANIES = [
    'inc', 'ltd', 'co', 'corp',
]

PLACES = [
    'arc', 'al', 'ave', "blv?d", 'cl', 'ct', 'cres', 'dr', "expy?", 'dist',
    'mt', 'ft', "fw?y", "hwa?y", 'la', "pde?", 'pl', 'plz', 'rd', 'st', 'tce',
    'Ala' , 'Ariz', 'Ark', 'Cal', 'Calif', 'Col', 'Colo', 'Conn', 'Del', 'Fed'
    , 'Fla', 'Ga', 'Ida', 'Id', 'Ill', 'Ind', 'Ia', 'Kan', 'Kans', 'Ken', 'Ky'
    , 'La', 'Me', 'Md', 'Is', 'Mass', 'Mich', 'Minn', 'Miss', 'Mo', 'Mont',
    'Neb', 'Nebr' , 'Nev', 'Mex', 'Okla', 'Ok', 'Ore', 'Penna', 'Penn', 'Pa'  ,
    'Dak', 'Tenn', 'Tex', 'Ut', 'Vt', 'Va', 'Wash', 'Wis', 'Wisc', 'Wy', 'Wyo',
    'USAFA', 'Alta' , 'Man', 'Ont', 'Qué', 'Sask', 'Yuk'
]

MONTHS = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','sept');
MISC = ( 'vs', 'etc', 'no', 'esp' );

ABBREVIATIONS = (@PEOPLE, @ARMY, @INSTITUTES, @COMPANIES, @PLACES, @MONTHS, @MISC )
