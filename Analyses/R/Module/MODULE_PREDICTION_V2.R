library(funHDDC)
library(funData)
library(fda)
library(fda.usc)
library(stringr)
library(Rcmdr)
library(factoextra)
library(FactoMineR)
setwd(dir = "C:/Users/1mduquesnoy/Downloads/BMX_race/Analyses/R")


###################################################################
# Name   :   Folder reading                                       #
# Date   :   01/07/2019                                           #
# Author :   Marc Duquesnoy                                       #
# Aim    :   Create the dataset from the file which should be     #
#            analysed by the fonctions below                      #
###################################################################


Creation_Test_Puissance = function(Name) {
  
  #Creation of the input XTest
  #Thus the output is a dataset with all the new powers to be predict.
  
  #param Name   : the name (as a string) of the file containing all the new trials
  
  X = read.csv(paste('Nouveaute/',Name,sep=""))
  
  ID = X[,1]
  Power_Test = X[,-1]
  
  return(list("X_Test"=Power_Test,"ID"=ID))
  
}
Creation_Test = function(Name) {
  
  ##Creation of the input XTest
  #Thus the output is a dataset with all the new feature to be predict.
  
  #param Name   : the name (as a string) of the file containing all the new trials
  
  X = read.csv(paste('Nouveaute/',Name,sep=""))
  
  ID = X[,1]
  Power_Test = X[,-1]
  
  return(list("X_Test"=Power_Test,"ID"=ID))
  
}






###################################################################
# Name   :   Classifcation_Puissance                              #
# Date   :   01/06/2019                                           #
# Author :   Marc Duquesnoy                                       #
# Aim    :   For new trials, it predict the power's class with a  #
#            result in Excel. Execute the functions below         #
###################################################################


Classification_Puissance = function(X_Test) {
  
  #For new trials, it predict the power's class
  #param : a P*N dataset containing all the new curves of power
  
  XTrain = read.csv("Module/XTrain_Puissance.csv",sep=";")
  YTrain = unlist(read.csv("Module/YTrain_Puissance.csv",sep=";"))
  
  dataf<-data.frame(as.factor(YTrain))
  x=fdata(XTrain)
  dat=list("df"=dataf,"x"=x)
  mod=classif.knn(as.factor(YTrain),x,knn=i)
  
  xx=fdata(X_Test)
  newdat<-list("x"=xx)
  p1<-predict.classif(mod,xx)
  
  return(p1)
  
  
}
Exportation = function(ID,Values,Name) {
  
  #Export in a csv, all the reuslts came down to your new trials
  
  #param ID      : a list with the informations about the identity of the trial
  #param Values  : a list with all the values from the model
  #param Name    : a string with the name of the file
  
  X = cbind(as.vector(ID),as.vector(Values))
  write.table(X, paste(paste("../Sorties_Modeles/",Name,sep=""),".csv",sep=""),
              row.names=FALSE, sep=";",dec=".", na=" ")
  
}



## Example ## do not execute

X_Test = Creation_Test_Puissance("Base_Ragot_P.csv")
mod = Classification_Puissance(X_Test$X_Test)
Exportation(X_Test$ID,mod,"Résultats_Power_Ragot_Juin")







###################################################################
# Name   :   Clustering                                           #
# Date   :   15/06/2019                                           #
# Author :   Marc Duquesnoy                                       #
# Aim    :   Find the best parameters for the unsupervised        #
#            classification of curves                             #
###################################################################


Clustering = function(X,k) {
  
  #Univariate clustering with functional data, find all the modeles as possible
  #param X : dataset J*Q where Q is the number of curve and J the length
  #param k : the number of clusters
  
  N=length(X[,1])
  P=length(X[1,])
  
  basis<- create.bspline.basis(c(0,1), nbasis=25)
  var1<-smooth.basis(argvals=seq(0,1,length.out = P),y=t(X),fdParobj=basis)$fd
  res.uni<-funHDDC(var1,K=1:k,model=c('AkBkQkDk','ABkQkDk', 'AkBQkDk', 'ABQkDk'),init="kmeans",threshold=0.2)
  
  print(res.uni$BIC)
  
  
}



###################################################################
# Name   :   Clustering_Best                                      #
# Date   :   15/06/2019                                           #
# Author :   Marc Duquesnoy                                       #
# Aim    :   Make an unsupervised classification of curves with   #
#            the best parameters from "Clustering". In output,    #
#            there is all individuals associated within their     #
#            class                                                #
###################################################################


Clustering_Best = function(X,model,k) {
  
  #Make a model with the best parameters found previously
  #param X     : dataset J*Q where Q is the number of curve and J the length
  #param k     : the number of clusters
  #param model : string with the name of the model
  
  N=length(X[,1])
  P=length(X[1,])
  
  basis<- create.bspline.basis(c(0,1), nbasis=25)
  var1<-smooth.basis(argvals=seq(0,1,length.out = P),y=t(X),fdParobj=basis)$fd
  res.uni<-funHDDC(var1,K=k,model=model,init="kmeans",threshold=0.2)
  
  return(list(mod=res.uni,class=res.uni$class))
}




## Example ## do not execute

X = Creation_Test("Test_Clustering.csv")
#X$X_Test[is.na(X$X_Test)] <- median(unlist(X$X_Test[4,]))
Clustering(X$X_Test,4)
clf = Clustering_Best(X$X_Test,"AKBQKDK",4)
Exportation(X$ID,clf$class,"Example_Clustering")


###################################################################
# Name   :   Projection_ACP                                       #
# Date   :   11/07/2019                                           #
# Author :   Marc Duquesnoy                                       #
# Aim    :   Show the projections of individuals with the new     #
#            pilots to be represented with others                 #
###################################################################


Projection_ACP = function(Labels,choix,axe1,axe2) {
  
  
  Data = read.csv('../Données/Frames/Base_Frames.csv',sep=";",header=TRUE)
  Data = subset(Data, select=c("DistanceRecul","DAlignementMin","DEpauleMin",                 
                               "DistanceDmin","EngagementDmin","HauteurFWRecul","Intention","HauteurFWDmin",
                               "ForceUPiedAvMax","ForceUPiedArMax","MoyennePuissanceButteTotale","MoyennePuissancePremCassure","PuissanceMaxPremCassure",
                               "TpsPassageGrille","TpsPremCassure","TpsBasDeButte","VitesseBasDeButte",
                               "ImpulsionParCoups","TravailParCoups","ImpulsionParCoups_1","TravailParCoups_1",
                               "ImpulsionParCoups_2","TravailParCoups_2","ImpulsionParCoups_3","TravailParCoups_3","ImpulsionParCoups_4",
                               "TravailParCoups_4","Time2Peak","Nom","Prenom","Numero","Date","Manivelle","Theta.Depart","Theta.Recul",                
                               "Braquet","Temps.Reaction","Explosivite"))
  
  
  N = length(Data[,1])
  P = length(Data[1,])
  Test = c()
  Labels_Init = c("Pilard_2018-06-21","Rencurel_2018-12-12","Ragot_2018-12-11","Mayet_2018-06-19","Mahieu_2018-12-13",
                  "Racine_2018-06-22","Andre_2018-12-12","Darnand_2018-06-21","Jouve_2018-06-20")
  Labels_Sup = c()
  Base_Init = c()
  
  for (i in 1:N) {
    
    if ( paste(as.vector(Data$Nom[i]), as.vector(Data$Date)[i],sep="_") %in% Labels_Init || paste(as.vector(Data$Nom[i]), as.vector(Data$Date)[i],sep="_") %in% Labels) {
      Base_Init = rbind(Base_Init,Data[i,])
    }
    
  }
  
  for (i in 1:length(Base_Init[,1])) {
    
    if ( paste(as.vector(Base_Init$Nom[i]), as.vector(Base_Init$Date)[i],sep="_") %in% Labels) {
      Labels_Sup = c(Labels_Sup,i)
    }
    
  }
  
  row_names = c()
  
  for (i in 1:length(Base_Init[,1])) {
    
    row_names[i] = paste(paste(as.vector(Base_Init$Nom)[i],as.vector(Base_Init$Numero)[i],sep="_"),substring(as.vector((Base_Init$Date))[i],6,10),sep = "")
    #row_names[i] = paste(paste(substring(as.vector(Base_Init$Nom)[i],1,3),as.vector(Base_Init$Numero)[i],sep="_"),substring(as.vector((Base_Init$Date))[i],6,10),sep="_")
    
  }
  
  rownames(Base_Init) = row_names
  Base_Init = Base_Init[ , ! colnames(Base_Init) %in% c("Nom","Prenom","Date","Numero")]
  
  res = PCA(Base_Init, scale.unit=TRUE, ncp=5, ind.sup=Labels_Sup, graph = FALSE)
  
  if (choix == "ind") {
    plot(fviz_pca_ind(res, axes = c(axe1,axe2), geom = c("point", "text"),
                      label = "all", invisible = "none", labelsize = 4,
                      pointsize = 2, habillage = "none",
                      col.ind = "#024efd", col.ind.sup = "#fb040b",
                      title = paste(paste("Visualisation des individus sur le plan princpal ",axe1,sep=""),axe2,sep="-"),
                      jitter = list(what = "label", width = NULL, height = NULL)))
  }
  
  else if (choix == "var") {
    
    plot(fviz_pca_var(res, axes = c(axe1,axe2), geom = c("arrow", "text"),
                      label = "all", invisible = "none", labelsize = 4,
                      col.var = "#012efe", col.quanti.sup = "blue",
                      title = paste(paste("Projection des variables sur le plan princpal ",axe1,sep=""),axe2,sep="-"),
                      select.var = list(name =NULL, cos2 = NULL, contrib = 25),
                      jitter = list(what = "label", width = NULL, height = NULL)))
    
  }
  
  
  return("Done") 
}



## Example ## do not run

Projection_ACP(c("Ragot_2018-06-22"),"ind",1,3)






