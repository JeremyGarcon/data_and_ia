import matplotlib.pyplot as plt

def Graphique_Température_Annuelle(Moyen_Température_Mensuelle):
    # Données
    x = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    y = [Moyen_Température_Mensuelle["Janvier"], Moyen_Température_Mensuelle["Février"], Moyen_Température_Mensuelle["Mars"], 
         Moyen_Température_Mensuelle["Avril"], Moyen_Température_Mensuelle["Mai"], Moyen_Température_Mensuelle["Juin"], 
         Moyen_Température_Mensuelle["Juillet"], Moyen_Température_Mensuelle["Août"], Moyen_Température_Mensuelle["Septembre"], 
         Moyen_Température_Mensuelle["Octobre"], Moyen_Température_Mensuelle["Novembre"], Moyen_Température_Mensuelle["Décembre"]]

    # Création du graphique
    plt.plot(x, y, marker='o', linestyle='-', color='b', label="Température")

    # Personnalisation
    plt.xlabel("Mois")
    plt.ylabel("Température Annuelle")
    plt.title("Graphique Annuel de Température")
    plt.legend()

    # Affichage
    Graphique_Température_Annuelle(Moyen_Température_Mensuelle)
    
    
    
def main():
    Graphique_Température_Annuelle(Moyen_Température_Mensuelle)
    Moyen_Température_Mensuelle = {
        "Janvier": 10,
        "Février": 20,
        "Mars": 25,
        "Avril": 30,
        "Mai": 40,
        "Juin": 35,
        "Juillet": 30,
        "Août": 25,
        "Septembre": 20,
        "Octobre": 15,
        "Novembre": 10,
        "Décembre": 5
    }
    
# Appel de la fonction   
main()
