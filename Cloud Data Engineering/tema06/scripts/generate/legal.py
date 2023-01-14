from faker import Faker

def get():
    fake = Faker('pt_BR')
    return [fake.company(), fake.lexify(text = '????'), fake.numerify(text = '##########0001')]