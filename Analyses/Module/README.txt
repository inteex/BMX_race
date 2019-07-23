Analyses/Module




############################################################

# Contenu                                                  #

############################################################




-DataManagement.py		: module Python contenant l'ensemble des fonctions nécessaires à la gestion des donnés.




-DataViz.py			: module Python contenant l'ensemble des fonctions nécessaires à la visualisation des analyses statistiques

					Barplot, SPM, ...


-Predictions.py 		: module Python contenant les fonctions de classifications/regressions utilisés pendant l'étude statistique



-Traitements_Statistiques_Users : srcipt Python utilisant l'ensemble des fonctions des modules. C'est uniquement

					ce script qui doit être utilisé par la personne désirant effectuer l'ensemble des analyses pour la suite. Il suffit de choisir

					quelle tâche exécuter, et de lancer le code associé.



- .csv                          : tous les fichiers CSV sont nécessaires au bon fonctionnement des modules. Ne pas les déplacer et ne pas les modifier/supprimer.



-DataCreationTestR              : module Python contenant l'ensemble des fonctions nécessaires à la création

					des bases de Test pour les fonctions R.





############################################################

# Remarques                                                #

############################################################



** L'utilisation du script necessite 2 choses :


			- connaitre l'environnement de travail, et de des données afin de le modifier en premières lignes de code.


			- connaitre les dates de passages associées aux essais des différents pilotes.



** Le module 'DataCreationTestR' ne doit être utilisé UNIQUEMENT que pour la création des bases de données tests

		nécessaires à l'utilisation des fonctions dans le module de prédictions sous R. L'ensemble des résultats de ce script Python

		envoie un fichier CSV dans le dossiers R/Nouveaute permettant d'y stocker les bases de données.





############################################################

# Descriptions des fonctions				   #

############################################################



*** DataManagement.py



	- Data_New_Predictions : fonction qui permet de creer une base de données test, utilisée par la suite si l'on souhaite effectuer une prédictions sur ces nouveaux essais par l'intermediaire du module
 
			Predictions.py. En entrée vous choisissez une liste d'essais effectués par des pilotes à une nouvelle date. Exemple : [Mayet_2018-12-12", "Darnand_2018-04-03", ...]



	- Data_Two_Pilots : fonction qui permet de créer les tableaux de données necessaires à l'utilisation de la fonction SPM_Comparaison. L'exemple dans 'Traitements_Statistiques_Users.py' illustre son utilisation.

	- Creation_Efficacite_3D_2D : fonction qui permet de créer les efficacités 3D et 2D necessaires pour la comparaison via la méthode SPM.





*** DataViz.py

	

	- Kiviat : compare 2 essais (pour 2 pilotes à 2 dates différentes, ou pour un même pilote sur 2 essais différents) pour les variables ["TimeToPeak","TpsBasDeButte","VitesseBasDeButte","DistanceRecul",

                   	"MoyennePuissancePremCassure"]. Si vous souhaitez changer ces variables, rentrez dans le code et changer les variables au deux seuls endroits où elles apparaissent.



	- Comparaison_Boxplot : affiche la répartition en histogramme, d'une variable, pour chaque pilote, afin de visualiser la valeur moyenne pour chacun d'entre eux.
 
		   	Cela tient compte des dates de passage de chaque pilote.



	- SPM_Comparaison : effectue un t-test paired avec des variables fonctionnelles, permettant de donner des différences significatives entre les essais d'une variables entre 2 groupes de pilotes, ou 2 pilotes.



	- Comparaion_Trials_Pilot : affiche une répartition sous forme d'histogramme, afin de comparer les 2 meilleurs essais face aux autres essais, pour des variables dites de gestuelles.

	
				


	** Afin de savoir quels essais comparer, tenez compte des exemples fournis dans Traitement_Statistiques_Users.py, en rentrant les noms des pilotes (chaine de caractère), les numeros d'essais (nombre entier),
 
			et les dates de passage (chaine decaractères).






*** Predictions.py



	- Predictions_Puissance_Explosivite : effectue la classification et la regression des nouveaux essais pour des pilotes, à partir d'une base de test formés par ces essais. En sortie, vous obtenez les valeurs

			de classes de puissances, associées aux essais, et la valeur de puissance au 1er coups de pédale, toujours associées au essais.

	- Lecture_XTest : exporte les résultats de la prédiction sous forme de CSV dont vous en choisisez le nom (chaine de caractère). Le fichier est automatiquement crée dans 'Sorties_Modèles'.

			Il suffit d'observer l'exemple et de choisir une liste de nouveaux essais grâce à la fonction 'Data_New_Predictions'.


	** Ce modèle se base sur les données 'frames' automatiquement concaténées pour les essais des pilotes à une date donnée.






*** DataCreationTestR.py


	- Creation_Test_Power : creation de la base de données necessaire à l'utilisation des scripts R, pour la prédiction du groupe associé à la courbe de puissance. Vous choisissez les nouveaux essais dont vous souhaitez predire
 
			ces classes, et en sortie la fonction crée AUTOMATIQUEMENT le fichier CSV que vous utiliserez sous R.

	- Creation_Test_Features : creation de la base de données necessaire à l'utilisation des scripts R, pour le clustering de courbes, sur une variable souhaitée, et pour des essais souhaités. Vous effectuez donc une

			classification de courbes pour une variables. La fonction crée AUTOMATIQUEMENT le fichier CSV que vous utiliserez sous R.





	** Ces 2 fonctions doivent être utilisées avant toute utilisation des scripts R, sinon vous ne possederez pas les bases de données (dans les fichiers CSV) nécessaires.






