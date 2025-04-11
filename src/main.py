from test_power import calculer_consommation_totale, graphique_consommation_mensuelle
from test_meteo import meteo_display_temperature_on_data , Graphique_Température_Annuelle
import pandas as pd


        
def main():
    
    
    # Power
    
    # File for data 
    file_power = "/home/garcon/Documents/github/data_and_ia/src/data/eCO2mix_RTE_Bretagne_Annuel-Definitif_2022.csv"  

    # Charger les données
    print("Chargement des données...")
    df = pd.read_csv(file_power, sep=',', quotechar='"', encoding='utf-8')


    # Calculer la consommation totale
    print("Calcul de la consommation totale...")
    total = calculer_consommation_totale(df)
    print(f"La consommation électrique totale en Bretagne pour 2022 est de {total:,.2f} MW")
    

    # Créer le graphique de consommation mensuelle
    print("Création du graphique de consommation mensuelle...")
    data_mensuelle = graphique_consommation_mensuelle(df)
    print("Graphique sauvegardé sous 'consommation_mensuelle_bretagne_2022.png'")
    
    
    # Meteo
    
    # File for data
    file_meteo = "/home/garcon/Documents/github/data_and_ia/src/data/donne_meteorologique.csv"
    
    # Charger les données
    print("Chargement des données météo...")
    df_meteo = pd.read_csv(file_meteo, sep=',', quotechar='"', encoding='utf-8')
    
    # Afficher la température sur les données
    print("Affichage de la température sur les données...")
    meteo_display_temperature_on_data(df_meteo)
    print("Graphique de température sur les données sauvegardé sous 'temperature_on_data.png'")
    
    

    
main()
