import re
from kegg.api import KeggAPI
from abc import ABC
from dataclasses import dataclass, field

@dataclass
class KeggObjectType(ABC):
    identifier: str


class Reaction(KeggObjectType):
    reactants: list[str] = field(default_factory=list)
    products: list[str] = field(default_factory=list)
    equation: str = None

    @property
    def reaction_id(self):
        return self.identifier

    @reaction_id.setter
    def reaction_id(self, value):
        if re.match(r'R\d{5}', value) is None:
            raise ValueError(f'{value} is not a valid reaction id')
        self.identifier = value

    def __init__(self,
                 reaction_id: str,
                 ):
        self.reaction_id = reaction_id
        self.extract_information()

    def extract_information(self) -> None:
        information: str = KeggAPI().get('reaction', self.reaction_id).text
        self.equation: str = re.search(r'EQUATION\s.*', information).group(0).replace('EQUATION', '')
        reactants, products = re.split(r'<?=>?', self.equation)
        self.reactants = re.findall(r'C\d{5}', reactants)
        self.products = re.findall(r'C\d{5}', products)

    def generate_edges(self) -> list[list[str, str]]:
        edges: list[list[str, str]] = list()
        if re.search(r'<=>', self.equation):
            for reactant in self.reactants:
                edges.extend([(reactant, self.reaction_id), (self.reaction_id, reactant)])
            for product in self.products:
                edges.extend([(product, self.reaction_id), (self.reaction_id, product)])
        if re.search(r'\s+=>', self.equation):
            for reactant in self.reactants:
                edges.append((reactant, self.reaction_id))
            for product in self.products:
                edges.append((self.reaction_id, product))
        return edges