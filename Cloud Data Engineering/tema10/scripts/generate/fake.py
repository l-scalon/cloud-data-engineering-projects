from faker import Faker

class Client():

    def __init__(self) -> None:
        pass

    def fake(self, type):
        fake = Faker('pt_BR')
        match type:
            case 'natural': return [fake.name(), fake.lexify(text = '???'), fake.numerify(text = '##########')]
            case 'legal': return [fake.company(), fake.lexify(text = '????'), fake.numerify(text = '##########0001')]