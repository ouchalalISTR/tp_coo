from django.db import models


class Departement(models.Model):
    numero = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"Departement numero : {self.numero}"

    def json(self):
        return {"numero": self.numero, "prix_m2": self.prix_m2, "id": self.id}

    def json_extended(self):
        return self.json()


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    def __str__(self):
        return f"Nom de la machine est : {self.nom}"

    def costs(self):
        return self.prix

    def json(self):
        return {"nom": self.nom, "prix": self.prix, "id": self.id}

    def json_extended(self):
        return self.json()


class Ingredient(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {"nom": self.nom, "id": self.id}

    def json_extended(self):
        return self.json()


class Prix(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    prix = models.IntegerField()

    def __str__(self):
        return f"Cout de {self.ingredient.nom} : {self.prix} euros/kg"

    def json(self):
        return {
            "ingredient": self.ingredient.nom,
            "departement": self.departement.numero,
            "prix": self.prix,
            "id": self.id,
        }

    def json_extended(self):
        return self.json()


class QuantiteIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.quantite} kg de {self.ingredient.nom}"

    def costs(self, departement):
        return (
            self.quantite
            * self.ingredient.prix_set.get(departement__numero=departement.numero).prix
        )

    def json(self):
        return {
            "ingredient": self.ingredient.nom,
            "quantite": self.quantite,
            "id": self.id,
        }

    def json_extended(self):
        return self.json()


class Action(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    commande = models.CharField(max_length=100)
    duree = models.IntegerField()
    ingredients = models.ManyToManyField(QuantiteIngredient)
    action = action = models.ForeignKey(
        "self", on_delete=models.PROTECT, blank=True, null=True, related_name="+"
    )

    def __str__(self):
        return f"Action : {self.commande}"

    def json(self):
        liste_ingredients = []
        for ing in self.ingredients.all():
            liste_ingredients.append(ing.ingredient.nom)
        return {
            "machine": self.machine.nom,
            "commande": self.commande,
            "duree": self.duree,
            "ingredients": liste_ingredients,
            "id": self.id
            # "action": self.action.id,
        }

    def json_extended(self):
        liste_ingredients = []
        for ingredient in self.ingredients.all():
            liste_ingredients.append(ingredient.json_extended())
        return {
            "machine": self.machine.json_extended(),
            "commande": self.commande,
            "duree": self.duree,
            "ingredients": liste_ingredients,
            # "action": self.action.json_extended(),
        }


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    def __str__(self):
        return f"Nom de la recette est : {self.nom}"

    def json(self):
        liste_ingredients = []
        for ing in self.action.ingredients.all():
            liste_ingredients.append(ing.ingredient.nom)
        return {"nom": self.nom, "action_ingredients": liste_ingredients, "id": self.id}

    def json_extended(self):
        return self.json()


class Usine(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    taille = models.IntegerField()
    machines = models.ManyToManyField(Machine)
    recettes = models.ManyToManyField(Recette)
    stocks = models.ManyToManyField(QuantiteIngredient)

    def __str__(self):
        return f"Usine (departement[{self.departement.numero}]) de {self.taille} m2"

    def costs(self):
        prix_usine = self.taille * self.departement.prix_m2
        prix_stocks = 0
        prix_machines = 0
        for machine in self.machines.all():
            prix_machines += machine.costs()
        for stock in self.stocks.all():
            prix_stocks += stock.costs(self.departement)
        return prix_usine + prix_machines + prix_stocks

    def json(self):
        liste_machines = []
        liste_recettes = []
        liste_stocks = []
        for machine in self.machines.all():
            liste_machines.append(machine.nom)
        for recette in self.recettes.all():
            liste_recettes.append(recette.nom)
        for stock in self.stocks.all():
            liste_stocks.append(stock.ingredient.nom)
        return {
            "departement": self.departement.numero,
            "taille": self.taille,
            "machines": liste_machines,
            "recettes": liste_recettes,
            "stocks": liste_stocks,
            "id": self.id,
        }

    def json_extended(self):
        liste_machines = []
        liste_recettes = []
        liste_stocks = []
        for machine in self.machines.all():
            liste_machines.append(machine.json_extended)
        for recette in self.recettes.all():
            liste_recettes.append(recette.json_extended)
        for stock in self.stocks.all():
            liste_stocks.append(stock.json_extended)
        return {
            "departement": self.departement.json_extended,
            "taille": self.taille,
            "machines": liste_machines,
            "recettes": liste_recettes,
            "stocks": liste_recettes,
        }
