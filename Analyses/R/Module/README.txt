Analyses/R/Modules


############################################################
# Contenu                                                  #
############################################################

- .csv	 	      : tous les fichiers CSv servent aux modules de prédictions. Il est interdit de les modifier,
			   supprimer, déplacer

- MODULE_PREDICTION.R : fichier R contenant l'ensemble des fonctions R permettant d'effectuer les analyses statistiques
			   prédictions, ...


## Remarque :

** Il est OBLIGATOIRE de lancer la fonction Python 'Creation_Test_Power' ou 'Creation_Test_Features' dans le module 'DataCreationTestR.py'
avec les pilotes souhaités par l'utilisateur afin de pouvoir utiliser les fonctions sur la classification des
courbes de Puissances, ou des courbes d'une autre variable.
Ce script Python crée les bases de données qui alimentent le code R.