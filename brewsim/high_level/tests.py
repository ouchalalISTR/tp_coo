from django.test import TestCase

from .models import (
    Action,
    Departement,
    Ingredient,
    Machine,
    Prix,
    QuantiteIngredient,
    Recette,
    Usine,
)


class MachineModelTests(TestCase):
    def test_usine_creation(self):
        self.assertEqual(Departement.objects.count(), 0)
        self.assertEqual(Machine.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)
        self.assertEqual(Action.objects.count(), 0)
        self.assertEqual(Usine.objects.count(), 0)

        departement_1 = Departement.objects.create(numero=31, prix_m2=2000)

        four = Machine.objects.create(nom="four", prix=1000)
        mash_tun = Machine.objects.create(nom="mash_tun", prix=2000)

        houblon = Ingredient.objects.create(nom="Houblon")
        orge = Ingredient.objects.create(nom="Orge")

        Prix.objects.create(ingredient=houblon, departement=departement_1, prix=20)
        Prix.objects.create(ingredient=orge, departement=departement_1, prix=10)

        stock_houblon = QuantiteIngredient.objects.create(
            ingredient=houblon, quantite=50
        )
        stock_orge = QuantiteIngredient.objects.create(ingredient=orge, quantite=100)

        houblon_witbier = stock_houblon
        houblon_witbier.quantite = stock_houblon.quantite / 2
        orge_witbier = stock_orge
        orge_witbier.quantite = stock_orge.quantite / 5

        ebullition = Action.objects.create(machine=four, commande="ebullition", duree=5)
        ebullition.ingredients.add(houblon_witbier)
        ebullition.ingredients.add(orge_witbier)

        witbier = Recette.objects.create(nom="Witbier", action=ebullition)

        usine = Usine.objects.create(departement=departement_1, taille=50)
        usine.machines.add(four)
        usine.machines.add(mash_tun)
        usine.recettes.add(witbier)
        usine.stocks.add(stock_houblon)
        usine.stocks.add(stock_orge)

        self.assertEqual(Departement.objects.count(), 1)
        self.assertEqual(Machine.objects.count(), 2)
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertEqual(Action.objects.count(), 1)
        self.assertEqual(Usine.objects.count(), 1)

        # print(f"Cout usine = {usine.costs()} ")
        print(f"cout d'usine est :{Usine.objects.first().costs()}")
