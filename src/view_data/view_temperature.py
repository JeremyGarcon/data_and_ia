import pandas as pd
import matplotlib.pyplot as plt


def view_temperature(
    fichier_csv,
    colonne_date="Date",
    colonne_temp="Temperature",
    date_debut="2022-01-01",
    date_fin="2022-09-31",
    afficher_graphique=False,
    Kelvin=True,
):
    """
    Analyse les températures journalières (moyenne, min, max) pour une période donnée.

    :param fichier_csv: Chemin du fichier CSV
    :param colonne_date: Nom de la colonne contenant les timestamps
    :param colonne_temp: Nom de la colonne contenant la température
    :param date_debut: Date de début (format AAAA-MM-JJ)
    :param date_fin: Date de fin (exclus, format AAAA-MM-JJ)
    :param afficher_graphique: True pour afficher un graphique
    :param Kelvin: True si les températures sont en Kelvin, False pour Celsius
    :return: DataFrame avec les stats par jour et éventuellement un graphique matplotlib
    """

    # 1. Charger les données
    try:
        df = pd.read_csv(fichier_csv, usecols=[colonne_date, colonne_temp])
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_csv} est introuvable.")
        return None, None
    except ValueError:
        print(f"Erreur : Les colonnes spécifiées ({colonne_date}, {colonne_temp}) sont introuvables.")
        return None, None

    # 2. Convertir la colonne date
    try:
        df[colonne_date] = pd.to_datetime(df[colonne_date], utc=True)
    except Exception as e:
        print(f"Erreur lors de la conversion de la colonne date : {e}")
        return None, None

    # 3. Filtrer la période
    try:
        debut = pd.Timestamp(date_debut, tz="UTC")
        fin = pd.Timestamp(date_fin, tz="UTC")
        df_filtered = df[(df[colonne_date] >= debut) & (df[colonne_date] < fin)]
    except Exception as e:
        print(f"Erreur lors du filtrage des dates : {e}")
        return None, None

    # 4. Grouper par jour
    df_filtered.set_index(colonne_date, inplace=True)
    if not Kelvin:
        df_filtered[colonne_temp] = df_filtered[colonne_temp] - 273.15

    stats_par_jour = df_filtered[colonne_temp].resample("D").agg(["mean", "min", "max"])

    print(f"Statistiques de température du {date_debut} au {date_fin} :")
    print(stats_par_jour)

    # 5. Graphique
    if afficher_graphique:
        fig, ax = plt.subplots(figsize=(12, 6))
        stats_par_jour["mean"].plot(ax=ax, label="Moyenne", marker="o", linestyle="-")
        stats_par_jour["min"].plot(ax=ax, label="Min", linestyle="--")
        stats_par_jour["max"].plot(ax=ax, label="Max", linestyle="--")

        if Kelvin:
            ax.set_title(f"Températures quotidiennes en degrés Kelvin : {date_debut} à {date_fin}")
        else:
            ax.set_title(f"Températures quotidiennes en degrés Celsius : {date_debut} à {date_fin}")

        ax.set_xlabel("Date")
        ax.set_ylabel("Température")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        # Retourner la figure et les statistiques par jour
        return stats_par_jour, fig
    else:
        return stats_par_jour, None


if __name__ == "__main__":
    stats, fig = view_temperature(
        fichier_csv="data/donne_meteorologique.csv",
        colonne_date="Date",
        colonne_temp="Temperature",
        date_debut="2022-01-01",
        date_fin="2022-09-30",
        afficher_graphique=True,
        Kelvin=False,
    )
    if fig:
        plt.show()
