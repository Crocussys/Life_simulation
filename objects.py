import random


class Creature:
    def __init__(self, gene):
        self.type = "creature"
        self.gene = gene
        self.energy = 0
        self.contains = []
        self.dead = False

    def next(self, cell, grid):
        if cell.temperature > int(self.gene[14:21], 2):
            self.dead = True
        if cell.temperature < int(self.gene[21:28], 2):
            self.dead = True
        if cell.height + 8000 > int(self.gene[28:42], 2):
            self.dead = True
        if cell.height + 8000 < int(self.gene[42:56], 2):
            self.dead = True
        if self.gene[2:4] == '00':
            if cell.distance != -1:
                energy = 1 - cell.distance / cell.sun.r
                cell.temperature -= energy
                self.energy += energy
            for obj in cell.contains:
                if obj.type == "element":
                    for elem in ["HHO", "COO", "N"]:
                        if obj.formula == elem and elem not in self.contains:
                            cell.contains.remove(obj)
                            self.contains.append(obj.formula)
                            break
            if "HHO" in self.contains and "COO" in self.contains and "N" in self.contains and self.energy >= 1:
                self.contains.remove("HHO")
                self.contains.remove("COO")
                self.contains.remove("N")
                self.energy -= 1
                cell.contains.append(Element("CHHON"))
                cell.contains.append(Element("OO"))
        if self.energy > int(self.gene[4:14], 2):
            self.energy = int(self.gene[4:14], 2)
        if self.energy >= int(self.gene[56:66], 2):
            neighboring_cell = grid.get_random_neighboring_cell(cell.pos)
            for obj in neighboring_cell.contains:
                if obj.type == "creature" and self.gene[2:4] != obj.gene[2:4]:
                    self.energy -= int(self.gene[56:66], 2)
                    new_gene = self.gene
                    if random.random() <= 0.01:
                        new_gene[random.randint(2, 66)] = str(random.randint(0, 1))
                    neighboring_cell.contains.append(Creature(new_gene))


class Element:
    def __init__(self, formula):
        self.type = "element"
        self.formula = formula
