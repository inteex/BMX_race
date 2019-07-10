Analyses/R/Modules


############################################################
# Contenu                                                  #
############################################################

- .csv	 	      : tous les fichiers CSv servent aux modules de pr�dictions. Il est interdit de les modifier,
			   supprimer, d�placer

- MODULE_PREDICTION.R : fichier R contenant l'ensemble des fonctions R permettant d'effectuer les analyses statistiques
			   pr�dictions, ...


## Remarque :

** Il est OBLIGATOIRE de lancer la fonction Python 'Creation_Test_Power' ou 'Creation_Test_Features' dans le module 'DataCreationTestR.py'
avec les pilotes souhait�s par l'utilisateur afin de pouvoir utiliser les fonctions sur la classification des
courbes de Puissances, ou des courbes d'une autre variable.
Ce script Python cr�e les bases de donn�es qui alimentent le code R.