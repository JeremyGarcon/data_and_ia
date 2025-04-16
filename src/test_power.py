import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Removed unused import

# Définir le chemin du fichier
file_path = "/home/garcon/Documents/github/data_and_ia/src/data/eCO2mix_RTE_Bretagne_Annuel-Definitif_2022.csv"  # Replace with your actual file path

# Fonction pour calculer la consommation totale
def calculer_consommation_totale(dataframe):
    """
    Calcule la consommation totale d'électricité à partir du dataframe.
    """
    # Convertir la colonne Consommation en numérique
    dataframe['Consommation'] = pd.to_numeric(dataframe['Consommation'], errors='coerce')
    
    # Calculer la somme totale (pas la moyenne)
    consommation_totale = dataframe['Consommation'].sum()
    
    return consommation_totale

# Fonction pour créer un graphique de consommation par mois
def graphique_consommation_mensuelle(dataframe):
    """
    Crée un graphique montrant la consommation mensuelle d'électricité.
    """
    # Convertir la colonne Date en datetime
    dataframe['Date'] = pd.to_datetime(dataframe['Date'], errors='coerce')
    
    # Extraire le mois à partir de la date
    dataframe['Mois'] = dataframe['Date'].dt.month
    
    # Créer un dictionnaire pour les noms des mois
    noms_mois = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 
        5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
        9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    
    # Grouper par mois et calculer la somme de consommation pour chaque mois
    consommation_mensuelle = dataframe.groupby('Mois')['Consommation'].sum().reset_index()
    
    # Ajouter une colonne avec le nom du mois
    consommation_mensuelle['Nom_Mois'] = consommation_mensuelle['Mois'].map(noms_mois)
    
    # Trier par numéro de mois
    consommation_mensuelle = consommation_mensuelle.sort_values('Mois')
    
    # Configurer le style du graphique
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Créer le graphique à barres
    ax = sns.barplot(x='Nom_Mois', y='Consommation', data=consommation_mensuelle, palette='viridis', hue='Nom_Mois', legend=False)
    
    # Ajouter les titres et labels
    plt.title('Consommation Électrique Totale par Mois en Bretagne (2022)', fontsize=15)
    plt.xlabel('Mois', fontsize=12)
    plt.ylabel('Consommation Totale (MW)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Ajouter les valeurs sur chaque barre
    for i, v in enumerate(consommation_mensuelle['Consommation']):
        ax.text(i, v/2, f"{v:,.0f}", ha='center', fontsize=10, color='white')
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Sauvegarder le graphique
    plt.savefig('consommation_mensuelle_bretagne_2022.png', dpi=300)
    
    # Afficher le graphique
    plt.show()
    
    return consommation_mensuelle

