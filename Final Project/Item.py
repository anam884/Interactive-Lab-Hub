class Item:
    def __init__(self, id, filename, stock, daysSinceLastSale):
        self.ID = id
        self.filename = "assets/clothes/" + filename + ".png"
        self.stock = int(stock)
        self.daysSinceLastSale = int(daysSinceLastSale)
    
    def checkConditions(self):
        return self.stock >= 100 or self.daysSinceLastSale >= 14


def GetAllItems():
    filename = "products.txt"
    items = []

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        print(filename)
        id, filename, stock, lastSale = line.split(",")
        lastSale = lastSale.rstrip()
        item = Item(id, filename, stock, lastSale)
        if item.checkConditions():
            items.append(item)

    return items
    