Analyses/R


############################################################
# Contenu                                                  #
############################################################

-Nouveaut�	    : Dossier contenant tous les fichiers CSV � utiliser pour les pr�dictions/classifications sous
			R. Ces fichiers proviennent du code Python qui cr�e les bases de donn�es.

-Module             : Dossier contenant l'ensemble des codes R (modules et fichier de traitement) permettant
			� l'utilisateur d'effectuer les analyses souhait�es.


############################################################
# Remarques                                                #
############################################################





############################################################
# Descriptions des fonctions				   #
############################################################

**** Folder reading

	- Creation_Test_Puissance : cr�ation de la base de test contenant les nouveaux essais � predire pour pr�dire les classes de Puissances associ�s � ces essais.
			L'argument d'entr�e est le nom du fichier CSV contenant les essais dans le fichier 'Nouveaut�'.

	- Creation_Test : cr�ation de la base de test contenant les nouveaux essais pour effectuer un clustering de courbes.
			L'argument d'entr�e est le nom du fichier CSV contenant les essais dans le fichier 'Nouveaut�'.



**** Classification_Puissance 

	- Classification_Puissance : effectue la pr�diction des classes avec la base issue de la fonction 'Creation_Test_Puissance'.

	- Exportation : exporte les resultats de cette classification, avec les identifiants et les classes obtenus. Il suffit de donner un nom pour le CSV de sortie.


**** Clustering


	- Clustering : affiche les param�tres optimaux du mod�le de classification de courbes. Pour cela, il faut choisir le nombre maximal de clusters que l'algorithme pourrait former.

	- Clustering_Best : effectue le clustering de courbes en utilisant en arguments d'entr�es, le 'model' et 'k' affich�s par la fonction pr�c�dente.


	** Il faut automatiquement lancer ces 2 fonctions � la suite afin d'effectuer une premi�re classification non optimale, puis de la refaire avec les param�tres optimaux.













