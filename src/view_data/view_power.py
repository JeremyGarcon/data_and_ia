import pandas as pd
import matplotlib.pyplot as plt
def analyser_consommation_par_jour(fichier_csv, colonne_date="Date", colonne_conso="Consommation",
                                   date_debut="2013-04-01", date_fin="2013-05-01", afficher_graphique=True):
    """
    Analyse la consommation énergétique quotidienne (moyenne, min, max) pour une période donnée.

    :param fichier_csv: Chemin du fichier CSV
    :param colonne_date: Nom de la colonne contenant les timestamps
    :param colonne_conso: Nom de la colonne contenant la consommation énergétique
    :param date_debut: Date de début (format AAAA-MM-JJ)
    :param date_fin: Date de fin (exclus, format AAAA-MM-JJ)
    :param afficher_graphique: True pour afficher un graphique
    :return: DataFrame avec les stats par jour
    """

    # 1. Charger les données
    try:
        df = pd.read_csv(fichier_csv, usecols=[colonne_date, colonne_conso], sep=",", on_bad_lines="skip")
    except ValueError as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return

    # 2. Convertir la colonne date
    df[colonne_date] = pd.to_datetime(df[colonne_date], errors="coerce", utc=True)

    # 3. Supprimer les lignes avec des valeurs NaN
    df.dropna(subset=[colonne_date, colonne_conso], inplace=True)

    # 4. Convertir la colonne consommation en numérique
    df[colonne_conso] = pd.to_numeric(df[colonne_conso], errors="coerce")
    df.dropna(subset=[colonne_conso], inplace=True)

    # 5. Filtrer la période
    debut = pd.Timestamp(date_debut, tz="UTC")
    fin = pd.Timestamp(date_fin, tz="UTC")
    df_filtered = df[(df[colonne_date] >= debut) & (df[colonne_date] < fin)]

    # 6. Grouper par jour
    df_filtered.set_index(colonne_date, inplace=True)
    stats_par_jour = df_filtered[colonne_conso].resample("D").agg(["mean", "min", "max"])

    # 7. Afficher les stats
    print(f"Statistiques de consommation énergétique du {date_debut} au {date_fin} :")
    print(stats_par_jour)

    # 8. Graphique
    if afficher_graphique:
        if stats_par_jour.empty:
            print("Aucune donnée disponible pour la période spécifiée.")
            return stats_par_jour

        plt.figure(figsize=(12, 6))
        stats_par_jour["mean"].plot(label="Moyenne")
        plt.title(f"Consommation énergétique quotidienne : {date_debut} à {date_fin}")
        plt.xlabel("Date")
        plt.ylabel("Consommation énergétique")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return stats_par_jour

# Exemple d'appel
analyser_consommation_par_jour("data/Power.csv", 
                               date_debut="2022-01-01", date_fin="2022-12-30", afficher_graphique=True)
