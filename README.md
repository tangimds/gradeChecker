# Grade Checker
## INSA Rennes
Script python qui vérifie, toutes les `x` minutes, si il y a une nouvelle note d'ajoutée sur l'ENT. Dans ce cas, un mail est envoyé avec la matière et la note correspondante.

## Getting Started

```
git clone https://gitlab.insa-rennes.fr/tangi.mendes/gradeChecker.git
```

### Prerequisites

python3
```
sudo apt install python3
```
pip
```
sudo apt install python3-pip
```

robobrowser (module python)
```
pip3 install robobrowser
```

### Run

Il faut laisser ce script tourner sur une machine.

```
./gradeChecker.py
```
## Exemple
Ensuite renseignez vos identifiants INSA. Par exemple :
```
~jlassalle$ ./gradeChecker.py
Merci de renseigner vos logins INSA.
user : jlassalle
mdp :
intervalle de verification (en minute) : 15

pas de nouvelle note
********************
* Message envoyé ! *
********************
done at 2019-01-15 13:11:44.414830

```

le mot de passe ne s'affichera pas sur la console, c'est normal.
Tapez le normalement et appuyez sur entrer.  
Vous pouvez utiliser les deux formats d'identifiant : `jlassale` ou `jean.lassalle`.  
Le script est alors lancé et affiche en console des messages à titre informatif, et vous envoie un mail sur votre boîte INSA.

### ne pas fermer la console, sinon le script ne tournera plus




## Author

* **Tangi Mendes** - *Initial work* - [gradeChecker](https://gitlab.insa-rennes.fr/Tangi.Mendes/gradeChecker)