Analyses/R


############################################################
# Contenu                                                  #
############################################################

-Nouveauté	    : Dossier contenant tous les fichiers CSV à utiliser pour les prédictions/classifications sous
			R. Ces fichiers proviennent du code Python qui crée les bases de données.

-Module             : Dossier contenant l'ensemble des codes R (modules et fichier de traitement) permettant
			à l'utilisateur d'effectuer les analyses souhaitées.


############################################################
# Remarques                                                #
############################################################





############################################################
# Descriptions des fonctions				   #
############################################################

**** Folder reading

	- Creation_Test_Puissance : création de la base de test contenant les nouveaux essais à predire pour prédire les classes de Puissances associés à ces essais.
			L'argument d'entrée est le nom du fichier CSV contenant les essais dans le fichier 'Nouveauté'.

	- Creation_Test : création de la base de test contenant les nouveaux essais pour effectuer un clustering de courbes.
			L'argument d'entrée est le nom du fichier CSV contenant les essais dans le fichier 'Nouveauté'.



**** Classification_Puissance 

	- Classification_Puissance : effectue la prédiction des classes avec la base issue de la fonction 'Creation_Test_Puissance'.

	- Exportation : exporte les resultats de cette classification, avec les identifiants et les classes obtenus. Il suffit de donner un nom pour le CSV de sortie.


**** Clustering


	- Clustering : affiche les paramètres optimaux du modèle de classification de courbes. Pour cela, il faut choisir le nombre maximal de clusters que l'algorithme pourrait former.

	- Clustering_Best : effectue le clustering de courbes en utilisant en arguments d'entrées, le 'model' et 'k' affichés par la fonction précédente.


	** Il faut automatiquement lancer ces 2 fonctions à la suite afin d'effectuer une première classification non optimale, puis de la refaire avec les paramètres optimaux.













