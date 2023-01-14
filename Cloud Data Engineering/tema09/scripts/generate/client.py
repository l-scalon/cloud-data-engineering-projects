from faker import Faker

class New():

    def __init__(self, type:str):
        self.type = type

    def fake(self):
        fake = Faker('pt_BR')
        match self.type:
            case 'natural': return [fake.name(), fake.lexify(text = '???'), fake.numerify(text = '##########')]
            case 'legal': return [fake.company(), fake.lexify(text = '????'), fake.numerify(text = '##########0001')]