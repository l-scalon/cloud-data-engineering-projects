from datetime import datetime
from bson import ObjectId

class Client():

    def __init__(self, type: str, name: str, documents: dict, id = None):
        self.id = id if id != None else ObjectId()
        self.type = type
        self.name = name
        self.documents = documents

    def build(self) -> dict:
        built_client = {"_id": self.id,
                       "type": self.type,
                       "name": self.name,
                       "documents": self.documents}
        return built_client        

class Transaction():

    def __init__(self, clientID: ObjectId, nature: str, type: str, time: datetime,
                    amount: float, id = None, tax = None, counterpart_id = None):
        self.id = id if id != None else ObjectId()
        self.clientID = clientID
        self.nature = nature
        self.type = type
        self.time = time
        self.amount = round(amount, 2)
        if tax != None:
            self.tax = tax if tax.get("rate") != 0 else None
        else: self.tax = self.set_tax()
        self.counterpart = counterpart_id

    def set_tax(self):
        match self.nature:
            case 'income':
                match self.amount:
                    case n if n <= 1000: return {"rate": 0.0001, "fee": round(self.amount * 0.0001, 2)}
                    case n if n <= 3000: return {"rate": 0.0003, "fee": round(self.amount * 0.0003, 2)}
                    case n if n <= 5000: return {"rate": 0.0005, "fee": round(self.amount * 0.0005, 2)}
                    case n if n <= 7000: return {"rate": 0.0007, "fee": round(self.amount * 0.0007, 2)}
                    case n if n > 7000: return {"rate": 0.0011, "fee": round(self.amount * 0.0011, 2)}
            case 'expense':
                match self.amount:
                    case n if n <= 1000: return None
                    case n if n <= 3000: return {"rate": 0.0001, "fee": round(self.amount * 0.0001, 2)}
                    case n if n <= 5000: return {"rate": 0.0003, "fee": round(self.amount * 0.0003, 2)}
                    case n if n <= 7000: return {"rate": 0.0005, "fee": round(self.amount * 0.0005, 2)}
                    case n if n > 7000: return {"rate": 0.0007, "fee": round(self.amount * 0.0007, 2)}

    def set_counterpart(self, counterpart_id):
        self.counterpart = counterpart_id

    def build(self) -> dict:
        built_transaction = {"_id": self.id,
                             "client": self.clientID,
                             "nature": self.nature,
                             "type": self.type,
                             "time": self.time,
                             "amount": self.amount}
        if self.tax != None: built_transaction["tax"] = self.tax
        if self.counterpart != None: built_transaction["transfer_counterpart"] = self.counterpart
        return built_transaction