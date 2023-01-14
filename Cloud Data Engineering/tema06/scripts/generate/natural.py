from faker import Faker

def get():
    fake = Faker('pt_BR')
    return [fake.name(), fake.lexify(text = '???'), fake.numerify(text = '##########')]
    