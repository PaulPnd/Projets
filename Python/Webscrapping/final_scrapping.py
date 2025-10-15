# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:18:03 2024

@author: pinard_p
"""

# Tous les imports relatifs à Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


# Import de Time pour eviter de se faie bloquer en passant de page par page
from time import sleep
# Import de Datetime pour savoir combien de temps le fichier met de temps à tourner
from datetime import datetime
# Import de pandas pour créer un dataframe qui sera exporter en fin de script
import pandas as pd
# Import de re pour pouvoir garder uniquement le mois de "Mai" + gérer les biographies d'artisites
import re
# Import de Counter pour les occurence de pronoms 
from collections import Counter


#####################################################################################
#####################################################################################

class ChoixClub:
    
    # Dans cette initialisation, on met le lien url des évènements passées pour 
    # chaque club que l'on souhaite scrap.
    # Ne pas oublier de rajouter le nombre de pages à scroll pour que l'on 
    # arrive sur les évènements voulus
    def __init__(self, nom_club):
        self.nom_club = nom_club.lower()
        self.clubs = {
            "rex": {"url": "https://fr.ra.co/clubs/1672/past-events", "nb_page_moins_un": 4},
            "macadam": {"url": "https://fr.ra.co/clubs/136779/past-events", "nb_page_moins_un": 2},
            "moulin rouge": {"url": "https://fr.ra.co/clubs/136779/past-events", "nb_page_moins_un": 2},
            "le sucre": {"url": "https://fr.ra.co/clubs/54145/past-events", "nb_page_moins_un": 2},
            "la machine": {"url": "https://fr.ra.co/clubs/28038/past-events", "nb_page_moins_un": 3},
            "concrete": {"url": "https://fr.ra.co/clubs/51836/past-events", "nb_page_moins_un": 3}
        }
    
    def choix_url(self):
        
        if self.nom_club in self.clubs:
            self.selected_club = self.clubs.get(self.nom_club, self.clubs)
            return self.selected_club
        else:
            raise ValueError(f"Error : Club {self.nom_club} n'existe pas !")

                    ####################################
                    ####################################
                    
class Lancement:
    def __init__(self,url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.driver.maximize_window()
    
        # Permet de récupérer un objet WebElement, essentiel pour faire des retours arrières 
    def get_driver(self):
        return self.driver
        
        
                    ####################################
                    ####################################

class Scrapping:
    
    def __init__(self,DRIVER):
        self.driver = DRIVER
        
        
    def WebDriverWait_element_click(self, class_name, chgmt_type_Class, stop = 0, temps_attente = 10):
        
        try:
            if chgmt_type_Class == "Link":
                element = WebDriverWait(self.driver, temps_attente).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, class_name))
                )
            else:
                element = WebDriverWait(self.driver, temps_attente).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, class_name))
                )
            return element
        except Exception:
            stop = 1
            return stop
        
    def WebDriverWait_element_loc(self, class_name, chgmt_type_Class, stop = 0):
        
        try:
            if chgmt_type_Class == "Link":
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, class_name))
                )
            else:
                element = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                )
            return element
        except Exception:
            stop = 1
            return stop
        
    def Liste_elem_Html(self, class_name, chgmt_type_Class, stop = 0):
        try:
            if chgmt_type_Class == "Link":
                element = self.driver.find_elements(By.LINK_TEXT, class_name)
            else:
                element = self.driver.find_elements(By.CLASS_NAME, class_name)
            return element
        except Exception:
            stop = 1
            return stop
        
    def Unique_elem_Html(self, class_name, chgmt_type_Class, stop = 0):
        try:
            if chgmt_type_Class == "Link":
                element = self.driver.find_element(By.LINK_TEXT, class_name)
            else:
                element = self.driver.find_element(By.CLASS_NAME, class_name)
            return element
        except Exception :
            stop = 1
            return stop
        
    def Click_Bouton(self, class_name = "Possible", chgmt_type_Class = "Rien", stop = 0, direct = "Non", temps = 10):
        
        if direct == "Non":
            Bouton = self.WebDriverWait_element_click(class_name, chgmt_type_Class, temps_attente=temps)
        else :
            Bouton = direct
        
        try:
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", Bouton)
            self.driver.execute_script("arguments[0].click();", Bouton)
            
            sleep(3)
            
        except Exception:
            stop = 1
            return(stop)
            
    def Scroll_Page(self,nb_page_moins_un):
        
        for Page in range(nb_page_moins_un):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            if Page == 0:
                try:
                    self.Click_Bouton(class_name = "Voir plus", chgmt_type_Class = "Link")
                except Exception as e:
                    print(e)
        
    def close(self):
        self.driver.quit()


                    ####################################
                    ####################################
                    
class formatage_donnees:
    
    # Ensemble des listes qui vont servir à créer notre base de données par la suite
    def __init__(self):
        self.Toutes_les_listes = {
            "Nom_club" : [],
            "Date_EV" : [],
            "Nom_EV" : [],
            "Annee_EV": [],

            "Infos_ART_Nom" : [],
            "Infos_ART_Exist_Bio":[],
            "Infos_ART_Pronoun" : [],
            "Infos_ART_LGBT" : [],
            "Infos_ART_Producteur" : [],
            "Infos_ART_Nb_Abo" : [],
            "Infos_ART_Feminisme" : [],
            "Infos_ART_Lien_Insta" : [],
            "Infos_ART_Deb_CA" : [],
            "Infos_ART_Lien_SoundCloud" : [],
            "Infos_ART_Localisation_Naissance" : [],
            "Infos_ART_Localisation_Base" : [],
            "Infos_ART_Ev_Participe" : [],
            "Infos_Region_1": [],
            "Infos_Region_2": [],
            "Infos_Region_3": [],
            "Infos_Region_4": [],
            "Infos_Region_5": [],
            "Infos_Asso_1": [],
            "Infos_Asso_2": [],
            "Infos_Asso_3": [],
            "Infos_Asso_4": [],
            "Infos_Asso_5": [],
            "Infos_Asso_6": [],
            "Infos_Apropos": [],
            "Infos_Pronoun_Spe": [],
            "Infos_Editorial": [],
            "Infos_Actualite": [],
            "Infos_Sexe_Determination": []
            }


    # Fonction pour nettoyer les artistes grisées que l'on récupère 
    # Pas parfait à 100% mais existe un autre moyen plus tard dans le script 
    # pour eviter que l'erreur passe jusqu'au bout 
    def clean_items(self, item_list, change_map = "No"):
        cleaned_list = []
        if change_map == "Yes":
            replace_map = {
                '/': ',', 
                '&': ',', 
                'b2b': ',',
                '+': ',', 
                'B2B': ','
            }
        else:
            replace_map = {
                '/': ',', 
                '&': ',', 
                'b2b': ',', 
                '-': ',', 
                '+': ',', 
                'B2B': ','
            }
        terms_to_remove = [
            'all night long', '- ODC live', '(live)', 'live', 'Extended Set',
            'Trip All Night Long', 'groovedge', 'bfdm', 'sound system', 
            'TTT', 'rephlex', 'in', 'side', '(2)', 'aka', 'Halle 1', 
            'Halle 2', 'Halle 3', 'Salle 1930', 'Does Disco', 
            'Esplanade: UQ-all stars','Esplanade', 'Le Sucre', 
            "' Ndagga Rhythm Force","Woodfloor:",
            "MAIN ROOM","Concrete:","Mainroom:",":"
        ]
        for item in item_list:
            # Replace les termes que l'on a mit dans la liste
            for key, value in replace_map.items():
                item = item.replace(key, value)
            
            # Retire les élements voulus 
            for term in terms_to_remove:
                item = re.sub(r'\b' + re.escape(term) + r'\b', '', item, flags=re.IGNORECASE)
            
            
            item = re.sub(r'\s*,\s*', ',', item.strip()) 
            item = re.sub(r',+', ',', item.strip(','))
            
            if item:
                cleaned_list.append(item.strip())
    
        return cleaned_list
    
    def ajout_val_liste(self,nom_liste,valeur):
        self.Toutes_les_listes[nom_liste].append(valeur)
    
    def recup_list(self,nom_liste):
        return self.Toutes_les_listes.get(nom_liste)
    
    def extract_month(self,text):
        text = text.lower()
        pattern = r'\b(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None


#####################################################################################
#####################################################################################

                ############### Infos ###############

# find_elements : Sort une liste de WebElement
# find_element : Sort le premier WebElement qui correspond à la demande 


# Macadam : Infos page 3 pour 2022 et page 2 pour 2019
# Rex : Infos page 4 pour 2022, page 4/5 pour 2019 et page 5 pour 2016
# Le Sucre : Infos page 3 pour 2022, page 3 pour 2019 et page 3 pour 2016

# Pour 8 evènements (Macadam 2022 ~ 8min de temps)
# Pour 20 évènements (Rex 2019 ~ 25 min de temps)


# Pour les tables en sortie de fichier, 
# Si un artiste ne possède pas de localisation alors sa page Perso n'existe plus !
# Si l'artiste possède une location mais pas de pronom + pas de ref + pas producteur alors 
# grande chance qu'il / elle ne possède tout simplement pas de Bio 


#####################################################################################
#####################################################################################

if __name__ == "__main__" :
    
    
    ################# Seule Partie à changer #########################
    
    page_club_choisi = "macadam"
    annee_to_check = ["2023"]
    
    ##################################################################
    
    print(datetime.now().time().strftime("%H:%M:%S")) 
    
    ##################################################################
    
    club_info = ChoixClub(page_club_choisi).choix_url()
    url = club_info["url"]
    nb_page_moins_un = club_info["nb_page_moins_un"]
    
    Crea_Df = formatage_donnees()
    
    scraper  = Scrapping(DRIVER = Lancement(url).get_driver())
    sleep(3)
    
    
    #### Début Première Loop
    for Annee in annee_to_check:
        
        print(Annee)
        sleep(2)
        Bordereau_Annee = scraper.Click_Bouton(class_name = "Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.Button__StyledAlignment-sc-51i17i-2.cQxpQc.lafiII.fzVkDX",
                                               chgmt_type_Class = "CLASS.NAME")
        
        lien_annee = scraper.Click_Bouton(class_name = Annee, chgmt_type_Class = "Link")
        
        scraper.Scroll_Page(nb_page_moins_un)
        
        evenement_loop = scraper.Liste_elem_Html("Box-sc-abq4qd-0.daeYCM","Class_Name")
        
        Liste_de_noms_evenements= []
        href_list = []
        
        #### Début Seconde Loop
        #### Loop pour récup infos Evenements
        for Evenements in range(len(evenement_loop)):
            
            Infos_Ev_liste = scraper.Liste_elem_Html("Box-sc-abq4qd-0.daeYCM","Class_Name")
            EV = Infos_Ev_liste[Evenements]
            print(EV.text)
            
            
            scraper_infos_EV = Scrapping(DRIVER = EV)
            recup_mois = scraper_infos_EV.Liste_elem_Html("Text-sc-wks9sf-0.loAMdA","Class_Name")
            
            # Premier Stoppeur 
            # On rentre dans la boucle seulement s'il y a des EV de récup
            if len(recup_mois) >= 1 :
                for mois in recup_mois:
                    
                    Mois_chgmt =  Crea_Df.extract_month(text = mois.text)
                    
                    if Mois_chgmt == "mai" or Mois_chgmt ==  "janv" : # Mois_chgmt == "mai" or "janv"
                        
                        artistes_EV = scraper_infos_EV.WebDriverWait_element_loc("Text-sc-wks9sf-0.Link__StyledLink-sc-1huefnz-0.jranq.kdgimZ", 
                                                                                 "Class_Name")
                        lien_href = artistes_EV.get_attribute("href")
                        nom_EV = scraper_infos_EV.WebDriverWait_element_loc("Box-sc-abq4qd-0.Heading__StyledBox-rnlmr6-0.daeYCM", 
                                                                                 "Class_Name")
                        nom_Club = scraper_infos_EV.WebDriverWait_element_loc("Text-sc-wks9sf-0.iXSpop", "Class_Name")

                        if nom_EV:
                            Crea_Df.ajout_val_liste("Nom_EV", nom_EV.text)
                            Crea_Df.ajout_val_liste("Date_EV", mois.text.lower())
                            Crea_Df.ajout_val_liste("Nom_club", nom_Club.text)
                            Crea_Df.ajout_val_liste("Annee_EV", Annee)
                            Liste_de_noms_evenements.append(nom_EV.text)
                            href_list.append(lien_href)
        #### Fin seconde Loop
        print("Fin Récup Infos Ev. Pause : 5 sec")
        sleep(5)
        
        nombre_Evenement_a_scrap = len(Liste_de_noms_evenements)
        
        #### Début Troisième Loop
        #### Loop pour récup infos Artistes
        #### Quand fin de 3eme loop, alors plus d'EV pour une annee X 
        for nombre_i in range(nombre_Evenement_a_scrap):
            
            print(f'Evenement {nombre_i + 1} / {nombre_Evenement_a_scrap}')
            
            Evenement_en_cours = Liste_de_noms_evenements[nombre_i]
            
            # Cas avec https://fr.ra.co/events/1522808
            # Ou Deux evenements avec EXACTEMENT le même nom sont présent sur la même page 
            # Donc obliger de vérifier aussi la date pour être sur de ce que l'on a  
            
            Test_plusieurs_EV_MM_noms = scraper.Liste_elem_Html(Evenement_en_cours, chgmt_type_Class = "Link")
            
            if len(Test_plusieurs_EV_MM_noms) > 1:
                for Evenement_i_meme_nom in Test_plusieurs_EV_MM_noms:
                    if Evenement_i_meme_nom.get_attribute("href") == href_list[nombre_i]:
                        scraper.Click_Bouton(direct=Evenement_i_meme_nom)
                        break
            else:
                scraper.Click_Bouton(class_name=Evenement_en_cours, chgmt_type_Class="Link")
            
            
            Boites_Artistes = scraper.WebDriverWait_element_loc("Text-sc-wks9sf-0.CmsContent__StyledText-sc-1s0tuo4-0.dzLFK.jjFEXj", 
                                                                "Class_Name")
            if Boites_Artistes == 1:
                Boites_Artistes = scraper.WebDriverWait_element_loc("Text-sc-wks9sf-0.CmsContent__StyledText-sc-1s0tuo4-0.guiqUO.jjFEXj", 
                                                                    "chgmt_type_Class")
            Boucle_liens_ART = Scrapping(DRIVER = Boites_Artistes).Liste_elem_Html("Link__AnchorWrapper-sc-1huefnz-1.kHGiqV", 
                                                                                 "Class_Name")
            href_DJ_list = []
            nombre_pr_lien = 0
            
            for A_liens in range(len(Boucle_liens_ART)):
                
                liste_artsites = Scrapping(DRIVER = Boites_Artistes).Liste_elem_Html("Link__AnchorWrapper-sc-1huefnz-1.kHGiqV", 
                                                                                     "Class_Name")
                Lien_X_artiste = liste_artsites[A_liens]
                href_DJ_list.append(Lien_X_artiste.get_attribute("href"))
                
            
            Boucle_Artistes = [musician.text.strip() for musician in Boucle_liens_ART]
            print(Boucle_Artistes)
            
            # Récupération de l'ensemble des artistes 
            # Même ceux qui sont grisée
            # Seront mis de côté juste après 
            # Besoin de faire des petites mises en formes 
            
            texte_raw = Boites_Artistes.text.split('\n')
            Ensemble_Artistes_Grise = Crea_Df.clean_items(texte_raw,change_map="Yes")
            
            print(Ensemble_Artistes_Grise)
            #### Début Quatrième Loop
            #### Boucle pour chaque lien d'artistes récup
            for art in Boucle_Artistes :
                
                
                nom_artiste =  art
                Possibilites_plusieurs_liens_mm_noms = scraper.Liste_elem_Html(nom_artiste,"Link")
                
                if len(Possibilites_plusieurs_liens_mm_noms) > 1:
                    for liens in Possibilites_plusieurs_liens_mm_noms:
                        if liens.get_attribute("href") == href_DJ_list[nombre_pr_lien]:
                            Artiste = scraper.Click_Bouton(direct=liens)
                            break
                else:
                    Artiste = scraper.Click_Bouton(class_name= nom_artiste, chgmt_type_Class= "Link")
                
                nombre_pr_lien += 1
                # Second Stoppeur
                if Artiste != 1:
                    
                    sleep(2)
                    Moment_Attente_bandereau  = scraper.WebDriverWait_element_loc("Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.kevYFu.lafiII",
                                                                       "Class_Name")
                    Moment_Attente_Page_Vide  = scraper.WebDriverWait_element_loc("Text-sc-wks9sf-0.kUHsCW",
                                                                       "Class_Name")
                    sleep(1)
                    Nom_A_Moment_attente = scraper.WebDriverWait_element_loc("Text-sc-wks9sf-0.etHNLC",
                                                                       "Class_Name")
                    
                    # Premier de la boucle pour le cas https://fr.ra.co/events/784808
                    # Second de la boucle pour le cas https://fr.ra.co/events/1049074
                    # Si bien du texte pour Moment_Attente_Page_Vide et 
                    # que l'on a pas de bandereau (Moment_Attente_bandereau == 1)
                    # alors premier cas
                    # Si on pas de texte pour Moment_Attente_Page_Vide et tjrs pas 
                    # de bandereau alors dans le second cas
                    if Moment_Attente_Page_Vide != 1 and Moment_Attente_bandereau == 1:
                       stop_retour_arrière = 0
                    elif Moment_Attente_bandereau == 1:
                        stop_retour_arrière = 1
                    else:
                        stop_retour_arrière = 0
                        
                    ## Troisième Stoppeur
                    if Moment_Attente_bandereau != 1:
                        
                        
                        Nom_de_artiste = Nom_A_Moment_attente.text
                        Crea_Df.ajout_val_liste("Infos_ART_Nom", Nom_de_artiste)
                        Crea_Df.ajout_val_liste("Infos_ART_Ev_Participe", Evenement_en_cours)
                        
                                                ####                          
                        Nb_Abo = scraper.Unique_elem_Html("Text-sc-wks9sf-0.iqKdpe", "Class_Name")
                        Crea_Df.ajout_val_liste("Infos_ART_Nb_Abo", Nb_Abo.text if Nb_Abo != 1 else 0)
                        
                                                ####                           
                        lien_Insta = scraper.Unique_elem_Html("Instagram", "Link")
                        Crea_Df.ajout_val_liste("Infos_ART_Lien_Insta", lien_Insta.get_attribute("href") if lien_Insta != 1 else "No Link")
                        
                                                ####    
                        lien_SD = scraper.Unique_elem_Html("Soundcloud", "Link")
                        Crea_Df.ajout_val_liste("Infos_ART_Lien_SoundCloud", lien_SD.get_attribute("href") if lien_SD != 1 else "No Link")
                            
                        Crea_Df.ajout_val_liste("Infos_ART_Deb_CA", scraper.Unique_elem_Html("Text-sc-wks9sf-0.hSZZee", "Class_Name").text)
                        
                        Localisation_ART = scraper.Liste_elem_Html(class_name = 'Text-sc-wks9sf-0.frbNeG', chgmt_type_Class = "ClassName")
                        if Localisation_ART != 1:
                            if len(Localisation_ART) > 0:
                                naissance = Localisation_ART[0].text
                                base = Localisation_ART[1].text if len(Localisation_ART) > 1 else naissance
                            else:
                                naissance = base = "No Localisation"
                        else:
                            naissance = base = "No Localisation"
                        
                        Crea_Df.ajout_val_liste("Infos_ART_Localisation_Naissance", naissance)
                        Crea_Df.ajout_val_liste("Infos_ART_Localisation_Base", base)

                        
                        Texte_Apropos = scraper.Unique_elem_Html(class_name = "Text-sc-wks9sf-0.CmsContent__StyledText-sc-1s0tuo4-0.jeSXW.jjFEXj", 
                                                                 chgmt_type_Class = "Class_Name")
                        if Texte_Apropos != 1:
                            Crea_Df.ajout_val_liste("Infos_Apropos", Texte_Apropos.text)
                        else:
                            Crea_Df.ajout_val_liste("Infos_Apropos", "Pas de partie 'A propos'")
                        
                        Nom_Ou_Pronom = scraper.Unique_elem_Html(class_name = "Box-sc-abq4qd-0.lmPJVg", 
                                                                 chgmt_type_Class = "Class_Name")
                        
                        SEXE = 'NA'
                        if Nom_Ou_Pronom != 1:
                            Zone_Pronoun_Specifie = scraper.Unique_elem_Html(class_name = "Text-sc-wks9sf-0.TextColumn__BreakText-qiu56k-0.jPcCND.fGrZvQ", 
                                                                     chgmt_type_Class = "Class_Name")
                            if Zone_Pronoun_Specifie != 1:
                                
                                Zone_texte = Zone_Pronoun_Specifie.text.lower()
                                
                                if re.search(r"\b(he|his|son|il)\b", Zone_texte, re.IGNORECASE):
                                    SEXE = 'M' 
                                elif re.search(r"\b(her|she|sa|elle)\b", Zone_texte, re.IGNORECASE):
                                    SEXE = 'F'
                                
                                if Nom_Ou_Pronom.text == "Vrai nom":
                                    
                                    ecrit_Pron_dans_nom = re.findall(
                                        r"\b(he|his|her|she|il|elle|they|them|iel)\b", 
                                                              Zone_texte, re.IGNORECASE)
                                    
                                    if ecrit_Pron_dans_nom:
                                        Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", sorted(set(map(str.lower, ecrit_Pron_dans_nom))))
                                        verif = 0
                                    else:
                                        Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", "Pas de 'Pronoms' dans zone spéciale")
                                        verif = 1
                                else:
                                    Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", Zone_Pronoun_Specifie.text)
                                    verif = 0
                            else :
                               Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", "Pas de zone spéciale 'Pronoms'") 
                               verif = 2
                        else:
                            Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", "Pas de zone spéciale 'Pronoms'")
                            verif = 2
                            
                        
                        
                            
                        ## Récupération des infos des lieux les plus visités 
                        ## Si moins de 5 lieux alors NA pour remplir
                        Box_reg = scraper.Unique_elem_Html("Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.fYEdpg.lafiII", "Class_Name")
                        Ensemble_listes_Reg = ["NA" for _ in range(5)]
                        if  Box_reg != 1:
                            Liste_reg = Scrapping(DRIVER=Box_reg).Liste_elem_Html("Link__AnchorWrapper-sc-1huefnz-1.fCdDZi", "Class_Name") 
                            for i in range(len(Liste_reg)):
                                Ensemble_listes_Reg[i] = Liste_reg[i].text
                        Crea_Df.ajout_val_liste("Infos_Region_1", Ensemble_listes_Reg[0])
                        Crea_Df.ajout_val_liste("Infos_Region_2", Ensemble_listes_Reg[1])
                        Crea_Df.ajout_val_liste("Infos_Region_3", Ensemble_listes_Reg[2])
                        Crea_Df.ajout_val_liste("Infos_Region_4", Ensemble_listes_Reg[3])
                        Crea_Df.ajout_val_liste("Infos_Region_5", Ensemble_listes_Reg[4])
                        
                        ## Récupération des artistes associés
                        ## Même méthode sauf qu'en certains gars n'ont pas 6 artistes Asso
                        ## Ou ont rien du tout 
                        ## Changement du Tag de la Box 
                        ## https://fr.ra.co/dj/braque
                        ## https://fr.ra.co/dj/modernhousequintet
                        Box_Bulles_Associes = scraper.WebDriverWait_element_loc(class_name="Grid__GridStyled-sc-si5izk-0.jZQJwh.Slide__ScrollArea-sc-1029lbb-0.jWXhPh",
                                                                                  chgmt_type_Class= "Class_Name")
                        
                        Ensemble_listes_Asso = ["NA" for _ in range(6)]
                        Nom_parties_bulles_associes = 0
                        if Box_Bulles_Associes == 1:
                            Box_Bulles_Associes = scraper.WebDriverWait_element_loc(class_name = "Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.SubSectionStacked__StyledAlignment-sc-erpxwz-0.dtgzXA.lafiII.iqPpDj",
                                                                                     chgmt_type_Class = "Class_Name")
                            Nom_parties_bulles_associes = Scrapping(DRIVER = Box_Bulles_Associes).WebDriverWait_element_loc(class_name= "Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.doCruk.lafiII", 
                                                                                            chgmt_type_Class = "Class_Name")
                            
                        if  Box_Bulles_Associes != 1 and Nom_parties_bulles_associes != 1:
                            if Nom_parties_bulles_associes == 0 or re.search(r"artistes associés",Nom_parties_bulles_associes.text,re.IGNORECASE):
                                Listes_Bulles_Associes = Scrapping(DRIVER = Box_Bulles_Associes).Liste_elem_Html("Column-sc-4kt5ql-0.Slide__Item-sc-1029lbb-1.cdoPJo.gQJkcc", 
                                                                                                               chgmt_type_Class = "Class_Name")
                                for i in range(len(Listes_Bulles_Associes)):
                                    Ensemble_listes_Asso[i] = Listes_Bulles_Associes[i].text.split('\n')[0]
                        Crea_Df.ajout_val_liste("Infos_Asso_1", Ensemble_listes_Asso[0])
                        Crea_Df.ajout_val_liste("Infos_Asso_2", Ensemble_listes_Asso[1])
                        Crea_Df.ajout_val_liste("Infos_Asso_3", Ensemble_listes_Asso[2])
                        Crea_Df.ajout_val_liste("Infos_Asso_4", Ensemble_listes_Asso[3])
                        Crea_Df.ajout_val_liste("Infos_Asso_5", Ensemble_listes_Asso[4])
                        Crea_Df.ajout_val_liste("Infos_Asso_6", Ensemble_listes_Asso[5])
                        
                        
                        bordereaux = scraper.Liste_elem_Html("Link__AnchorWrapper-sc-1huefnz-1.kHGiqV.SubNavLink__StyledSubNavLink-ld7eyt-0.VLvxV",
                                                             "Class_Name")
                        boucle_bordereau = 0
                        emplacement_lien_bio = 99
                        deja_infos_lists_A = 0
                        deja_infos_lists_E = 0
                        for bio_acces in bordereaux:
                                if bio_acces.text == "Biographie":
                                    emplacement_lien_bio = boucle_bordereau
                                if bio_acces.text == "Actualités RA":
                                    Crea_Df.ajout_val_liste("Infos_Actualite", "Oui")
                                    deja_infos_lists_A = 1
                                if bio_acces.text == "Éditorial RA":
                                    Crea_Df.ajout_val_liste("Infos_Editorial", "Oui")
                                    deja_infos_lists_E = 1
                                boucle_bordereau += 1
                        if deja_infos_lists_A == 0:
                            Crea_Df.ajout_val_liste("Infos_Actualite", "Non")
                        if deja_infos_lists_E == 0:
                            Crea_Df.ajout_val_liste("Infos_Editorial", "Non")
                            
                        Lien_Bio = scraper.Click_Bouton(direct = bordereaux[emplacement_lien_bio]) if emplacement_lien_bio != 99 else 1

                        ## Quatrième Stoppeur 
                        if Lien_Bio != 1:
                            bio_selenium = scraper.WebDriverWait_element_loc("Text-sc-wks9sf-0.CmsContent__StyledText-sc-1s0tuo4-0.eoRtSu.jjFEXj",
                                                                          "Class_Name")
                            ## Cinquième Stoppeur 
                            if bio_selenium != 1:
                                
                                bio_texte = bio_selenium.text.lower()
                                
                                pronoun_match = re.findall(
                                    r"\b(he|his|her|she|il|elle|they|them|iel)\b", 
                                                          bio_texte, re.IGNORECASE)
                                ref_lgbt_match = re.findall(
                                    r"\b(lgbtq+|lgbt|flinta|trans|queer|gay|lesbian|butch)\b", 
                                                           bio_texte, re.IGNORECASE)
                                producteur_match = re.findall(
                                    r"\b(producer|ep|album|producteur|productrice)\b", 
                                                           bio_texte, re.IGNORECASE)
                                Feminisme_match = re.findall(
                                    r"\b(féminisme|feminism|inclusif|intersectionnel|intersectionnal)\b", 
                                                           bio_texte, re.IGNORECASE)
                                
                                # Crea_Df.ajout_val_liste("Infos_Sexe_Determination", SEXE) 
                                if pronoun_match:
                                    Crea_Df.ajout_val_liste("Infos_ART_Pronoun", sorted(set(map(str.lower, pronoun_match))))
                                    pronoun_counts = Counter(map(str.lower, pronoun_match))
    
                                    # Get the most frequent pronoun
                                    most_common_pronoun, count = pronoun_counts.most_common(1)[0]
                                    
                                    # Assign SEXE based on the most frequent pronoun
                                    if SEXE == "NA":  # Only update if SEXE hasn't been determined yet
                                        if most_common_pronoun in {"iel"}:
                                            SEXE = 'Non Binaire'
                                        elif most_common_pronoun in {"her", "she", "elle"}:
                                            SEXE = 'F'
                                        elif most_common_pronoun in {"his", "he", "il"}:
                                            SEXE = 'M'
                                        else:
                                            SEXE = 'NA'
                                else:
                                    Crea_Df.ajout_val_liste("Infos_ART_Pronoun", "No pronoun")
                                    
                                Crea_Df.ajout_val_liste("Infos_ART_LGBT", sorted(set(map(str.lower, ref_lgbt_match))) if ref_lgbt_match else "No LGBT Ref")
                                Crea_Df.ajout_val_liste("Infos_ART_Feminisme", sorted(set(map(str.lower, Feminisme_match))) if Feminisme_match else "No Feminisme Ref")
                                Crea_Df.ajout_val_liste("Infos_ART_Producteur", sorted(set(map(str.lower, producteur_match))) if producteur_match else "Not Producteur")
                                Crea_Df.ajout_val_liste("Infos_ART_Exist_Bio", "Oui")

                                
                            else:
                                Crea_Df.ajout_val_liste("Infos_ART_Pronoun", "No pronoun")
                                Crea_Df.ajout_val_liste("Infos_ART_LGBT", "No LGBT Ref")
                                Crea_Df.ajout_val_liste("Infos_ART_Producteur", "Not Producteur")
                                Crea_Df.ajout_val_liste("Infos_ART_Feminisme", "No Feminisme Ref")
                                Crea_Df.ajout_val_liste("Infos_ART_Exist_Bio", "Non")
                            ## Fin Cinquième Stoppeur 
                                
                            # Ce premier retour en arrère est pour revenir à la page principale de l'artiste X
                            scraper.driver.back()
                            sleep(3)    
                            scraper.driver.execute_script("window.scrollTo(0, 0);")
                            sleep(2)
                            
                            # ***************************** # 
                           
                        else:
                            Crea_Df.ajout_val_liste("Infos_ART_Pronoun", "No pronoun")
                            Crea_Df.ajout_val_liste("Infos_ART_LGBT", "No LGBT Ref")
                            Crea_Df.ajout_val_liste("Infos_ART_Producteur", "Not Producteur")
                            Crea_Df.ajout_val_liste("Infos_ART_Feminisme", "No Feminisme Ref")
                            Crea_Df.ajout_val_liste("Infos_ART_Exist_Bio", "Non")
                        ## Fin Quatrième Stoppeur
                        
                        if SEXE == "NA":
                            if verif != 0 :
                                
                                data_prenom = pd.read_csv("Prenoms.csv", sep=';', encoding='latin1')
                                Mots_importants = ["daddy", "mama", "brother"]
                                alias_nom = scraper.Unique_elem_Html(class_name = "Text-sc-wks9sf-0.CmsContent__StyledText-sc-1s0tuo4-0.jrnVxy.jjFEXj", 
                                                                     chgmt_type_Class = "Class_Name")
                                
                                if verif == 1 :
                                        
                                    Nom_Prenoms = Zone_texte.split(" ")
                                    
                                    for Names in Nom_Prenoms:
                                        
                                        pattern = r'\b' + re.escape(Names) + r'\b'
                                        match_row = data_prenom[data_prenom['01_prenom'].str.contains(pattern, case=False, na=False)].iloc[:1]
                                        
                                        if not match_row.empty:
                                            
                                            SEXE = match_row.iloc[0]['02_genre'].upper()
                                            break
                                        
                                if SEXE == 'NA':
                                    
                                    Nom_de_Art  = Nom_de_artiste.split(" ")
                                    
                                    for Parts in Nom_de_Art:
                                            
                                        pattern_sec = r'\b' + re.escape(Parts) + r'\b'
                                        match_row_sec = data_prenom[data_prenom['01_prenom'].str.contains(pattern_sec, case=False, na=False)].iloc[:1]
                                        
                                        if not match_row_sec.empty:
                                            
                                            SEXE = match_row_sec.iloc[0]['02_genre'].upper()
                                            break
                                        
                                    if SEXE == 'NA':
                                        keyword_Match = re.search(r"|".join(Mots_importants), Nom_de_artiste, re.IGNORECASE)
                                        
                                        if keyword_Match:
                                            matched_text = keyword_Match.group()  
                                            if re.search(r"\b(daddy|brother)\b", matched_text, re.IGNORECASE):
                                                SEXE = 'M'
                                            elif re.search(r"\b(mama)\b", matched_text, re.IGNORECASE):
                                                SEXE = 'F'
                                            else:
                                                SEXE = 'NA'
                                    
                                if alias_nom != 1 and SEXE == 'NA':
                                    
                                    Alias_de_Art  = alias_nom.text.split(" ")
                                    
                                    for Parts in Alias_de_Art:
                                            
                                        pattern_sec = r'\b' + re.escape(Parts) + r'\b'
                                        match_row_sec = data_prenom[data_prenom['01_prenom'].str.contains(pattern_sec, case=False, na=False)].iloc[:1]
                                        
                                        if not match_row_sec.empty:
                                            
                                            SEXE = match_row_sec.iloc[0]['02_genre'].upper()
                                            break
                                    
                                    if SEXE == 'NA':
                                        keyword_Match = re.search(r"|".join(Mots_importants), alias_nom.text, re.IGNORECASE)
                                        
                                        if keyword_Match:
                                            matched_text = keyword_Match.group()
                                            if re.search(r"\b(daddy|brother)\b", matched_text, re.IGNORECASE):
                                                SEXE = 'M'
                                            elif re.search(r"\b(mama)\b", matched_text, re.IGNORECASE):
                                                SEXE = 'F'
                                            else:
                                                SEXE = 'NA'
                                            
                        Crea_Df.ajout_val_liste("Infos_Sexe_Determination", SEXE) 
                        
                    # On récupère le nom de l'artiste qui n'a plus de page perso de cette manière 
                    else:
                        Crea_Df.ajout_val_liste("Infos_ART_Nom", nom_artiste)
                        Crea_Df.ajout_val_liste("Infos_ART_Nb_Abo", "NA")
                        Crea_Df.ajout_val_liste("Infos_Sexe_Determination", "No GENRE") 
                        Crea_Df.ajout_val_liste("Infos_ART_Pronoun", "No pronoun")
                        Crea_Df.ajout_val_liste("Infos_ART_LGBT", "No LGBT Ref")
                        Crea_Df.ajout_val_liste("Infos_ART_Producteur", "Not Producteur")
                        Crea_Df.ajout_val_liste("Infos_ART_Feminisme", "No Feminisme Ref")
                        Crea_Df.ajout_val_liste("Infos_ART_Lien_Insta", "No Link")
                        Crea_Df.ajout_val_liste("Infos_ART_Lien_SoundCloud", "No Link")
                        Crea_Df.ajout_val_liste("Infos_ART_Deb_CA", "NA")
                        Crea_Df.ajout_val_liste("Infos_ART_Localisation_Naissance", "No Localisation")
                        Crea_Df.ajout_val_liste("Infos_ART_Localisation_Base", "No Localisation")
                        Crea_Df.ajout_val_liste("Infos_ART_Ev_Participe", Evenement_en_cours)
                        Crea_Df.ajout_val_liste("Infos_Region_1", "NA")
                        Crea_Df.ajout_val_liste("Infos_Region_2", "NA")
                        Crea_Df.ajout_val_liste("Infos_Region_3", "NA")
                        Crea_Df.ajout_val_liste("Infos_Region_4", "NA")
                        Crea_Df.ajout_val_liste("Infos_Region_5", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_1", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_2", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_3", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_4", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_5", "NA")
                        Crea_Df.ajout_val_liste("Infos_Asso_6", "NA")
                        Crea_Df.ajout_val_liste("Infos_ART_Exist_Bio", "Non")
                        Crea_Df.ajout_val_liste("Infos_Apropos", "Pas de partie 'A propos'")
                        Crea_Df.ajout_val_liste("Infos_Actualite", "Pas de partie 'Actualite'")
                        Crea_Df.ajout_val_liste("Infos_Editorial", "Pas de partie 'Editorial'")
                        Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", "Pas de zone spéciale 'Pronoms'")
                    ## Fin Troisième Stoppeur
                    
                    # Ce retour en arrière est pour revenir à l'évènement avec l'ensemble des artistes dessus
                    # Ce back() est dans le if car si le code n'a pas réussi à rentrer dans le if()
                    # Cela veut dire de la même manière qu'il n'a pas réussit à cliquer sur un artiste
                    # Donc pas besoin de revenir en arrière
                    # Sauf cas ou un lien existe mais pas cliquable quand même donc check avant 
                    if stop_retour_arrière == 0 :
                        scraper.driver.back()
                        sleep(1)
                        scraper.driver.execute_script("window.scrollTo(0, 0);")
                        sleep(1)
                sleep(2)
                
            #### Fin Quatrième Loop
            split_list = Ensemble_Artistes_Grise[0].split(',')
            Ensemble_Artistes_Grise_filtree = [art for art in split_list if not any(name in art for name in Boucle_Artistes)]
            print(Ensemble_Artistes_Grise_filtree)
            print("***")
            
            for nb_Art_grise in range(len(Ensemble_Artistes_Grise_filtree)):
                Crea_Df.ajout_val_liste("Infos_ART_Nom", Ensemble_Artistes_Grise_filtree[nb_Art_grise])
                Crea_Df.ajout_val_liste("Infos_ART_Nb_Abo", "NA")
                Crea_Df.ajout_val_liste("Infos_Sexe_Determination", "NA") 
                Crea_Df.ajout_val_liste("Infos_ART_Pronoun", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_LGBT", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Producteur", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Feminisme", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Lien_Insta", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Lien_SoundCloud", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Deb_CA", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Localisation_Naissance", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Localisation_Base", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Ev_Participe", Evenement_en_cours)
                Crea_Df.ajout_val_liste("Infos_Region_1", "NA")
                Crea_Df.ajout_val_liste("Infos_Region_2", "NA")
                Crea_Df.ajout_val_liste("Infos_Region_3", "NA")
                Crea_Df.ajout_val_liste("Infos_Region_4", "NA")
                Crea_Df.ajout_val_liste("Infos_Region_5", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_1", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_2", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_3", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_4", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_5", "NA")
                Crea_Df.ajout_val_liste("Infos_Asso_6", "NA")
                Crea_Df.ajout_val_liste("Infos_ART_Exist_Bio", "NA")
                Crea_Df.ajout_val_liste("Infos_Apropos", "NA")
                Crea_Df.ajout_val_liste("Infos_Actualite", "NA")
                Crea_Df.ajout_val_liste("Infos_Editorial", "NA")
                Crea_Df.ajout_val_liste("Infos_Pronoun_Spe", "NA")
            
            # On revient sur la page avec l'ensemble des evènements pour l'année X du club Y
            scraper.driver.back()
            sleep(2)
            
            bordereaux_liste_evenement = scraper.Liste_elem_Html("Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.cRRqoZ.lafiII", 
                                                                 "Class_Name")
            boucle_bordereau_Zero = 0
            emplacement_lien_EV_passes = 99
            for retour_point_zero in bordereaux_liste_evenement:
                if retour_point_zero.text == "Evénements passés":
                    emplacement_lien_EV_passes = boucle_bordereau_Zero 
                boucle_bordereau_Zero += 1
            
            Remise_Zero = scraper.Click_Bouton(direct = bordereaux_liste_evenement[emplacement_lien_EV_passes])
            
            Bouton_Annee = scraper.Click_Bouton(class_name= "Box-sc-abq4qd-0.Alignment-sc-1405w7f-0.Button__StyledAlignment-sc-51i17i-2.cQxpQc.lafiII.fzVkDX",
                                                  chgmt_type_Class= "CLASS.NAME")
            lien_Annee = scraper.Click_Bouton(class_name= Annee, chgmt_type_Class= "Link")
            scraper.Scroll_Page(1)
            sleep(3)
        #### Fin Troisième Loop
        
        sleep(2)
        scraper.driver.back()
    #### Fin Première Loop
    
    scraper.close()
    
    # Dictionnaire pour créer des futures tables
    dict_Evenement = {'Nom_Evenement': Crea_Df.recup_list("Nom_EV"), 
                      'Date_Evenement': Crea_Df.recup_list("Date_EV"), 
                      'Nom_Club_Evenement': Crea_Df.recup_list("Nom_club"),
                      'Annee_Evenement': Crea_Df.recup_list("Annee_EV")} 

    dict_Artiste = {'Nom_Artiste': Crea_Df.recup_list("Infos_ART_Nom"), 
                    'Nom_Evenement': Crea_Df.recup_list("Infos_ART_Ev_Participe"), 
                    'Endroit_Naissance': Crea_Df.recup_list("Infos_ART_Localisation_Naissance"),
                    'Endroit_Habitat': Crea_Df.recup_list("Infos_ART_Localisation_Base"), 
                    'Nombre_Abonnees': Crea_Df.recup_list("Infos_ART_Nb_Abo"),
                    'Annee_Premiere_EV': Crea_Df.recup_list("Infos_ART_Deb_CA"),
                    'Lien_Insta': Crea_Df.recup_list("Infos_ART_Lien_Insta"),
                    'Lien_Soundcloud': Crea_Df.recup_list("Infos_ART_Lien_SoundCloud"),
                    'Artiste_Pronom_Specifie': Crea_Df.recup_list("Infos_Pronoun_Spe"),
                    'Pronoms_Biographie': Crea_Df.recup_list("Infos_ART_Pronoun"),
                    'Genre_attribuer': Crea_Df.recup_list("Infos_Sexe_Determination"),  
                    'Mention_LGBT': Crea_Df.recup_list("Infos_ART_LGBT"), 
                    'Mention_Producteur': Crea_Df.recup_list("Infos_ART_Producteur"),
                    'Reg_Plus_Present': Crea_Df.recup_list("Infos_Region_1"),
                    'Sec_Reg_Plus_Pres': Crea_Df.recup_list("Infos_Region_2"),
                    'Trois_Reg_Plus_Pres': Crea_Df.recup_list("Infos_Region_3"),
                    'Quatr_Reg_Plus_Pres': Crea_Df.recup_list("Infos_Region_4"),
                    'Cinq_Reg_Plus_Pres': Crea_Df.recup_list("Infos_Region_5"),
                    'Artiste_Asso_1': Crea_Df.recup_list("Infos_Asso_1"),
                    'Artiste_Asso_2': Crea_Df.recup_list("Infos_Asso_2"),
                    'Artiste_Asso_3': Crea_Df.recup_list("Infos_Asso_3"),
                    'Artiste_Asso_4': Crea_Df.recup_list("Infos_Asso_4"),
                    'Artiste_Asso_5': Crea_Df.recup_list("Infos_Asso_5"),
                    'Artiste_Asso_6': Crea_Df.recup_list("Infos_Asso_6"),
                    'Artiste_Bio_Existe': Crea_Df.recup_list("Infos_ART_Exist_Bio"),
                    'Artiste_Actualite_Existe': Crea_Df.recup_list("Infos_Actualite"),
                    'Artiste_Editorial_Existe': Crea_Df.recup_list("Infos_Editorial"),
                    'Artiste_Texte_Apropos': Crea_Df.recup_list("Infos_Apropos")} 


    df_Evenement = pd.DataFrame(dict_Evenement)
    #df_Evenement.to_excel(f"{page_club_choisi}_Evenement_{annee_to_check[0]}_{annee_to_check[-1][-2:]}.xlsx")

    df_Artiste = pd.DataFrame(dict_Artiste)
    #df_Artiste.to_excel(f"{page_club_choisi}_Artiste_{annee_to_check[0]}_{annee_to_check[-1][-2:]}.xlsx")
    
    merged_df = pd.merge(df_Evenement, df_Artiste, on='Nom_Evenement')
    merged_df.to_excel(f"{page_club_choisi}_{annee_to_check[0]}_{annee_to_check[-1][-2:]}.xlsx")
    
    
    
    ##################################################################
    
    print(datetime.now().time().strftime("%H:%M:%S")) 
    
    ##################################################################