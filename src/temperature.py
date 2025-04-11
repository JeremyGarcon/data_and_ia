import pandas as pd
import matplotlib.pyplot as plt

def analyser_temperature_par_jour(fichier_csv, colonne_date="Date", colonne_temp="Temperature",
                                   date_debut="2022-08-01", date_fin="2022-08-25", afficher_graphique=True, Kelvin=True):
    """
    Analyse les températures journalières (moyenne, min, max) pour une période donnée.

    :param fichier_csv: Chemin du fichier CSV
    :param colonne_date: Nom de la colonne contenant les timestamps
    :param colonne_temp: Nom de la colonne contenant la température
    :param date_debut: Date de début (format AAAA-MM-JJ)
    :param date_fin: Date de fin (exclus, format AAAA-MM-JJ)
    :param afficher_graphique: True pour afficher un graphique
    :return: DataFrame avec les stats par jour
    """

    # 1. Charger les données
    df = pd.read_csv(fichier_csv, usecols=[colonne_date, colonne_temp])

    # 2. Convertir la colonne date
    df[colonne_date] = pd.to_datetime(df[colonne_date], utc=True)

    # 3. Filtrer la période
    debut = pd.Timestamp(date_debut, tz="UTC")
    fin = pd.Timestamp(date_fin, tz="UTC")
    df_filtered = df[(df[colonne_date] >= debut) & (df[colonne_date] < fin)]

    # 4. Grouper par jour
    df_filtered.set_index(colonne_date, inplace=True)
    if Kelvin == False:
        df_filtered.loc[:, colonne_temp] = df_filtered[colonne_temp] - 273.15

    stats_par_jour = df_filtered[colonne_temp].resample("D").agg(["mean", "min", "max"])

    # 5. Afficher les stats
    print(f"Statistiques de température du {date_debut} au {date_fin} :")
    print(stats_par_jour)

    # 6. Graphique
    if afficher_graphique:
        plt.figure(figsize=(12, 6))
        stats_par_jour["mean"].plot(label="Moyen", marker="o", linestyle="-")
        stats_par_jour["min"].plot(label="Min", linestyle='--')
        stats_par_jour["max"].plot(label="Max", linestyle='--')
        if Kelvin:
            plt.title(f"Températures quotidiennes en degrés Kelvin : {date_debut} à {date_fin}")
        else:
            plt.title(f"Températures quotidiennes en degrés Celsius : {date_debut} à {date_fin}")

        plt.xlabel("Date")
        plt.ylabel("Température")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return stats_par_jour

analyser_temperature_par_jour("/home/garcon/Documents/github/data_and_ia/src/data/donne_meteorologique.csv", 
                              date_fin="2022-08-03T17", date_debut="2022-07-11T13", afficher_graphique=False, Kelvin=False)
