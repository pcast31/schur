#première version de Nested monte carlo
#mise en commun vendredi avec les autres élèves du groupe
#ce porgramme utilise une classe arbre non présente sur ce fichier

import random
from arbre import Arbre


#k correspond au nombre d'ensemble autorisés
#dict_init correspond à un dictionnaire initial de valeurs
def NMC(dict_init,max_dict_init,profondeur,k):#max_k_dict):
    best_result=dict_init#dictionnaire correspondant au résultat à cette étape
    nbre_suivant=max_dict_init+1# nbre uivant à insérer
    best_score=nbre_suivant-1#meilleur score trouvé
    dico_optimal={}#meilleure partition trouvée
    dic_opt={}#stocke localement les dictionnaires pour ensuite les comparer
    result_max=0#stocke le dictionniare où sera insérer la prochaine valeur
    while result_max!=-1:#not(check_final(best_result,k,nbre_suivant)):
        score_max=nbre_suivant-1# score obtenu avec cette configuration
        result_max=-1
        if profondeur == 1:
            for i in range(k): #on regarde quelle place doit avoir l'élement nbre_suivant pour optimiser le score
                if check(best_result,i,nbre_suivant):
                    score,new_dict=score_max2(best_result,nbre_suivant,i,5,k)
                    if score>=score_max:
                        score_max=score
                        result_max=i
                        dic_opt=new_dict



        else:
            for i in range(k):##on regarde quelle place doit avoir l'élement nbre_suivant pour optimiser le score
                if check(best_result,i,nbre_suivant):
                    dico=best_result.copy()
                    dico[nbre_suivant]=i
                    score,new_dict=NMC(dico,nbre_suivant,profondeur-1,k)#appel récursif
                    if score>=score_max:
                        score_max=score
                        result_max=i
                        dic_opt=new_dict



        

        
        if profondeur==3:
            print("profondeur3",nbre_suivant)
    
        if score_max > best_score:#enregistre le nouveau meilleur score s'il existe
            best_score=score_max
            dico_optimal=dic_opt.copy()

        if result_max>=0: #si l'insertion est possible, on adapte le résultat
            insertion_suivante=result_max
            best_result[nbre_suivant]=insertion_suivante
            nbre_suivant+=1


    return best_score,dico_optimal




def score_max2(dico,nbre_suivant,l_insert,nbre_essai,k):
    sous_arbre=Arbre(dico,k)
    maxi=0
    mean=0
    arb=sous_arbre
    for i in range(nbre_essai):
        val,arbval=ajout_alea2(sous_arbre,l_insert,nbre_suivant)
        mean+=val
        maxi=max(maxi,val)
        if val==maxi:
            arb=arbval
    return maxi,arb.get_valeur()

def ajout_alea2(sous_arbre,l_insert,nbre_suivant):#explore l'arbre aléatoirement
    if not(check(sous_arbre.get_valeur(),l_insert,nbre_suivant)):# si la profondeur est maximale, on la retourne
        return nbre_suivant-1,sous_arbre
    l_alea=random.randint(0,sous_arbre.nbre-1)
    sous_arbre.cree_fils(nbre_suivant,l_insert) #la boucle while augmente fortement le temps de calcul mais donne de meilleurs résultats
    while not(check(sous_arbre.get_fils(l_insert).get_valeur(),l_alea,nbre_suivant+1)) and not(check_final(sous_arbre.get_fils(l_insert).get_valeur(),sous_arbre.nbre,nbre_suivant+1)): 
        l_alea=random.randint(0,sous_arbre.nbre-1)
        sous_arbre.cree_fils(nbre_suivant,l_alea)
    return ajout_alea2(sous_arbre.get_fils(l_insert),l_alea,nbre_suivant+1) #appel récursif pour calculer la nouvelle profondeur



def check(dico,nbre_liste,element): #vérfie si on peut insérer element dans l'ensemble nbre_liste étant donné un dico
    for nbre in dico:
        if dico[element-nbre]==nbre_liste and dico[nbre]==nbre_liste and element!=2*nbre:
            return False
    return True

def check_final(dico,k,element): #vérifie si element est insérable dans une liste
    for i in range(k):
        if check(dico,i,element):
            return False
    return True


def verification(dico,k):#vérifie qu'une partition est correcte
    res={}
    for i in range(k):
        res[i]=[]
    for nbre in dico:
        res[dico[nbre]].append(nbre)
    for i in res:
        l=res[i]
        for val1 in l:
            for val2 in l:
                if val1 !=val2 and val1+val2 in l:
                    print(val1,val2,val1+val2)
                    return False
    return True


dict_schur3={1:0,2:0,3:1,4:0,5:1,6:1,7:1,8:0,9:2,10:2,11:0,12:2,13:2,14:2,15:2,16:2,17:2,18:2,19:1,20:2,21:1,22:0,23:1}
dict_schur4={1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 0, 9: 2, 10: 2, 11: 0, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2, 19: 1, 20: 2, 21: 1, 22: 0, 23: 1, 24: 3, 
25: 0, 26: 3, 27: 3, 28: 3, 29: 3, 30: 3, 31: 3, 32: 0, 33: 3, 34: 3, 35: 3, 36: 1, 37: 0, 38: 1, 39: 3, 40: 3, 41: 3, 42: 3, 43: 3, 44: 0, 45: 3, 46: 3, 47: 3, 48: 
3, 49: 3, 50: 1, 51: 1, 52: 1, 53: 0, 54: 2, 55: 2, 56: 2, 57: 2, 58: 0, 59: 2, 60: 2, 61: 2, 62: 2, 63: 0, 64: 1, 65: 1, 66: 1}
dict_schur5={1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 0, 9: 2, 10: 2, 11: 0, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2, 19: 1, 20: 2, 21: 1, 22: 0, 23: 1, 24: 3, 25: 3, 26: 3, 27: 0, 28: 3, 29: 3, 30: 3, 31: 3, 32: 0, 33: 1, 34: 1, 35: 1, 36: 3, 37: 0, 38: 3, 39: 3, 40: 3, 41: 3, 42: 0, 43: 3, 44: 3, 45: 3, 46: 3, 47: 0, 48: 3, 49: 1, 50: 1, 51: 1, 52: 0, 53: 2, 54: 2, 55: 2, 56: 2, 57: 0, 58: 2, 59: 2, 60: 2, 61: 2, 62: 0, 63: 1, 64: 1, 65: 1, 66: 4, 67: 0, 68: 4, 69: 4, 70: 4, 71: 4, 
72: 4, 73: 4, 74: 4, 75: 4, 76: 4, 77: 0, 78: 4, 79: 1, 80: 0, 81: 4, 82: 4, 83: 4, 84: 4, 85: 4, 86: 0, 87: 4, 88: 4, 89: 1, 90: 1, 91: 4, 92: 4, 93: 4, 94: 2, 95: 
2, 96: 3, 97: 4, 98: 3, 99: 4, 100: 3, 101: 2, 102: 4, 103: 3, 104: 1, 105: 4, 106: 4, 107: 4, 108: 4, 109: 4, 110: 4, 111: 4, 112: 4, 113: 4, 114: 4, 115: 4, 116: 4, 117: 4, 118: 4, 119: 4, 120: 4, 121: 4, 122: 4, 123: 4, 124: 4, 125: 4, 126: 0, 127: 4, 128: 4, 129: 4, 130: 4, 131: 4, 132: 4, 133: 1, 134: 1, 135: 1, 136: 0, 137: 2, 138: 2, 139: 2, 140: 2, 141: 2, 142: 2, 143: 2, 144: 2, 145: 2, 146: 0, 147: 1, 148: 1, 149: 1, 150: 3, 151: 0, 152: 3, 153: 3, 154: 3, 155: 3, 156: 3, 157: 3, 
158: 3, 159: 3, 160: 1, 161: 3, 162: 3, 163: 3, 164: 3, 165: 3, 166: 3, 167: 0, 168: 3, 169: 3, 170: 3, 171: 3, 172: 0, 173: 3, 174: 1, 175: 1, 176: 1, 177: 0, 178: 
2, 179: 2, 180: 2, 181: 2, 182: 0, 183: 2, 184: 2, 185: 2, 186: 2, 187: 0, 188: 1, 189: 1, 190: 1}

dict_bis=dict_schur4.copy()
for i in range(66,2*66+1):
    dict_bis[i]=4

print(NMC(dict_bis,2*66,3,5))
