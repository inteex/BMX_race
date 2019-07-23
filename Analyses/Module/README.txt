Analyses/Module




############################################################

# Contenu                                                  #

############################################################




-DataManagement.py		: module Python contenant l'ensemble des fonctions n�cessaires � la gestion des donn�s.




-DataViz.py			: module Python contenant l'ensemble des fonctions n�cessaires � la visualisation des analyses statistiques

					Barplot, SPM, ...


-Predictions.py 		: module Python contenant les fonctions de classifications/regressions utilis�s pendant l'�tude statistique



-Traitements_Statistiques_Users : srcipt Python utilisant l'ensemble des fonctions des modules. C'est uniquement

					ce script qui doit �tre utilis� par la personne d�sirant effectuer l'ensemble des analyses pour la suite. Il suffit de choisir

					quelle t�che ex�cuter, et de lancer le code associ�.



- .csv                          : tous les fichiers CSV sont n�cessaires au bon fonctionnement des modules. Ne pas les d�placer et ne pas les modifier/supprimer.



-DataCreationTestR              : module Python contenant l'ensemble des fonctions n�cessaires � la cr�ation

					des bases de Test pour les fonctions R.





############################################################

# Remarques                                                #

############################################################



** L'utilisation du script necessite 2 choses :


			- connaitre l'environnement de travail, et de des donn�es afin de le modifier en premi�res lignes de code.


			- connaitre les dates de passages associ�es aux essais des diff�rents pilotes.



** Le module 'DataCreationTestR' ne doit �tre utilis� UNIQUEMENT que pour la cr�ation des bases de donn�es tests

		n�cessaires � l'utilisation des fonctions dans le module de pr�dictions sous R. L'ensemble des r�sultats de ce script Python

		envoie un fichier CSV dans le dossiers R/Nouveaute permettant d'y stocker les bases de donn�es.





############################################################

# Descriptions des fonctions				   #

############################################################



*** DataManagement.py



	- Data_New_Predictions : fonction qui permet de creer une base de donn�es test, utilis�e par la suite si l'on souhaite effectuer une pr�dictions sur ces nouveaux essais par l'intermediaire du module
 
			Predictions.py. En entr�e vous choisissez une liste d'essais effectu�s par des pilotes � une nouvelle date. Exemple : [Mayet_2018-12-12", "Darnand_2018-04-03", ...]



	- Data_Two_Pilots : fonction qui permet de cr�er les tableaux de donn�es necessaires � l'utilisation de la fonction SPM_Comparaison. L'exemple dans 'Traitements_Statistiques_Users.py' illustre son utilisation.

	- Creation_Efficacite_3D_2D : fonction qui permet de cr�er les efficacit�s 3D et 2D necessaires pour la comparaison via la m�thode SPM.





*** DataViz.py

	

	- Kiviat : compare 2 essais (pour 2 pilotes � 2 dates diff�rentes, ou pour un m�me pilote sur 2 essais diff�rents) pour les variables ["TimeToPeak","TpsBasDeButte","VitesseBasDeButte","DistanceRecul",

                   	"MoyennePuissancePremCassure"]. Si vous souhaitez changer ces variables, rentrez dans le code et changer les variables au deux seuls endroits o� elles apparaissent.



	- Comparaison_Boxplot : affiche la r�partition en histogramme, d'une variable, pour chaque pilote, afin de visualiser la valeur moyenne pour chacun d'entre eux.
 
		   	Cela tient compte des dates de passage de chaque pilote.



	- SPM_Comparaison : effectue un t-test paired avec des variables fonctionnelles, permettant de donner des diff�rences significatives entre les essais d'une variables entre 2 groupes de pilotes, ou 2 pilotes.



	- Comparaion_Trials_Pilot : affiche une r�partition sous forme d'histogramme, afin de comparer les 2 meilleurs essais face aux autres essais, pour des variables dites de gestuelles.

	
				


	** Afin de savoir quels essais comparer, tenez compte des exemples fournis dans Traitement_Statistiques_Users.py, en rentrant les noms des pilotes (chaine de caract�re), les numeros d'essais (nombre entier),
 
			et les dates de passage (chaine decaract�res).






*** Predictions.py



	- Predictions_Puissance_Explosivite : effectue la classification et la regression des nouveaux essais pour des pilotes, � partir d'une base de test form�s par ces essais. En sortie, vous obtenez les valeurs

			de classes de puissances, associ�es aux essais, et la valeur de puissance au 1er coups de p�dale, toujours associ�es au essais.

	- Lecture_XTest : exporte les r�sultats de la pr�diction sous forme de CSV dont vous en choisisez le nom (chaine de caract�re). Le fichier est automatiquement cr�e dans 'Sorties_Mod�les'.

			Il suffit d'observer l'exemple et de choisir une liste de nouveaux essais gr�ce � la fonction 'Data_New_Predictions'.


	** Ce mod�le se base sur les donn�es 'frames' automatiquement concat�n�es pour les essais des pilotes � une date donn�e.






*** DataCreationTestR.py


	- Creation_Test_Power : creation de la base de donn�es necessaire � l'utilisation des scripts R, pour la pr�diction du groupe associ� � la courbe de puissance. Vous choisissez les nouveaux essais dont vous souhaitez predire
 
			ces classes, et en sortie la fonction cr�e AUTOMATIQUEMENT le fichier CSV que vous utiliserez sous R.

	- Creation_Test_Features : creation de la base de donn�es necessaire � l'utilisation des scripts R, pour le clustering de courbes, sur une variable souhait�e, et pour des essais souhait�s. Vous effectuez donc une

			classification de courbes pour une variables. La fonction cr�e AUTOMATIQUEMENT le fichier CSV que vous utiliserez sous R.





	** Ces 2 fonctions doivent �tre utilis�es avant toute utilisation des scripts R, sinon vous ne possederez pas les bases de donn�es (dans les fichiers CSV) n�cessaires.






