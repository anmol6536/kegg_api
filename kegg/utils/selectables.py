from enum import Enum


class KeggObjects(Enum):
    PATHWAY = 'pathway'
    KO = 'ko'
    REACTION = 'reaction'
    COMPOUND = 'compound'
    BRITE = 'brite'
    MODULE = 'module'
    DISEASE = 'disease'
    DRUG = 'drug'
    ENVIRON = 'environ'
    GENOME = 'genome'
    GENES = 'genes'