import numpy as np

"""
DISCLAIMER : Ceci n'est pas une implémentation de Bouzy mais une implémentation de l'algorithme Nested Monte Carlo Search présenté
dans l'article de Eliahou et al. Nous avons décidé, pour être plus à l'aise avec Monte Carlo, de commencer par là. Nous nous reverrons
vendredi 12 février pour tout mettre en commun et mettre au point une version "propre" de Bouzy.

DISCLAIMER 2 : La plupart du programme vient de Thibaut, j'ai travaillé sur cette base car je n'étais vraiment pas à l'aise avec les
classes. Mon seul travail ici a été d'implémenter la fonction nested2 qui applique NMC à un niveau quelconque à partir du travail de
Thibaut qui l'avait déjà implémenté pour un NMC de niveau 1
"""


class Arbre:
    nbre = 3

    def __init__(self, partition, depth):
        self.partition = partition
        self.depth = depth
        self.fils = [None for i in range(Arbre.nbre)]
        self.height = 0

    def show(self):
        """Renvoie la liste des partitions terminales"""
        k = 0
        lst = []
        for f in self.fils:
            if f == None:
                k += 1
            else:
                lst += f.show()
        if k == Arbre.nbre:
            return [self.partition]
        else:
            return lst

    def __str__(self):
        return str(self.show())

    def insert(self, valeur, p):
        """Insère un fils avec une partition spécifiée à la position k"""
        if self.fils[p] == None:
            self.fils[p] = Arbre(valeur, self.depth + 1)

    def get_valeur(self):
        return self.partition

    def __getitem__(self, k):
        """Permet d'obtenir le fils k avec des []"""
        return self.fils[k]

    def legal(self, k):
        """Teste si on peut ajouter le prochain entier dans la classe k"""
        for i in range(1, self.depth+1):
            if self.partition[i] == k and self.partition[self.depth+1-i] == k and i != self.depth+1-i:
                return False
        return True

    def add(self, k):
        """Rajoute un fils légal spécifié"""
        valeur = self.partition.copy()
        valeur[self.depth + 1] = k
        self.insert(valeur, k)

    def expanse(self):
        """Rajoute un fils légal quelqconque"""
        for k in range(Arbre.nbre):
            if self.legal(k):
                self.add(k)

    def simulate(self):
        """Explore l'arbre aléatoirement jusqu'à trouver une feuille"""
        next = []
        n = 0
        for k in range(Arbre.nbre):
            if self.legal(k):
                n += 1
                next.append(k)
        if n == 0:
            pass
        else:
            k = np.random.randint(0, n)
            self.add(next[k])
            self[next[k]].simulate()

    def height_func(self):
        """Renvoie la hauteur de l'arbre"""
        next = []
        n = 0
        for f in self.fils:
            if f == None:
                n += 1
            else:
                next.append(f)
        if n == Arbre.nbre:
            return 1
        else:
            return 1 + max([f.height_func() for f in next])

    def explore(self, k):
        """Itère la fonction simulate et calcule la hauteur de l'arbre"""
        for _ in range(k):
            self.simulate()
        self.height = self.height_func()


def nested(a):
    next = []
    n = 0
    for k in range(Arbre.nbre):
        if a.legal(k):
            n += 1
            next.append(k)
    lst = []
    if n > 0:
        for k in range(len(next)):
            a.add(next[k])
            a[next[k]].simulate()
            lst.append(a[next[k]].height)
        b = np.argmax(lst)
        nested(a.fils[next[b]])
    a.height = a.height_func()


def nested2(a, level):
    """Explore et construit un arbre de partitions faiblement sans-sommes à partir de l'arbre a à l'aide de la méthode
    de Nested Monte Carlo au niveau level"""
    lst = []
    next = []
    if level == 1:
        nested(a)  # Cas de base
    else:
        for k in range(Arbre.nbre):
            if a.legal(k):
                a.add(k)  # On construit les fils
                next.append(k)
                # On applique NMC à l'ordre level - 1 aux fils en faisant un appel récursif
                nested2(a[k], level-1)
                lst.append(a[k].height)
        if lst != []:
            b = np.argmax(lst)  # On choisit le fils qui maximise la profondeur
            # On applique notre fonction à l'ordre level à ce fils
            nested2(a.fils[next[b]], level)
    a.height = a.height_func()


a = Arbre({1: 0}, 1)
nested2(a, 3)
print(a.height)  # On construit un arbre de partitions à 3 sous-ensembles. On obtient une borne inférieure de 22 ou 23 le plus souvent
# Bon signe puisque WS(3) = 23
