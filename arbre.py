class Arbre:
    def __init__(self, valeur,k):
        self.racine = valeur
        self.fils=[None for i in range(k)]
        self.nbre=k


    def insert(self, valeur,p):
            self.fils[p] = Arbre(valeur,self.nbre)


    def get_valeur(self):
        return self.racine

    def get_fils(self,p):
        return self.fils[p]

    def cree_fils(self,nbre_suivant,l_couleur):
        val_fils=self.get_valeur().copy()
        val_fils[nbre_suivant]=l_couleur
        self.insert(val_fils,l_couleur)
