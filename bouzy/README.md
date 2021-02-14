## Remarques générales
- Cette version manque de tests et de commentaires. Ils seront ajoutés prochainement.
- La fonction fillEndCol n'a pas été ajoutée pour l'instant.
- L'algorithme abstractSimulation n'a pas encore été implémenté.

## Remarque sur l'implémentation
- Les algorithmes CoreRWS, RWS et DFS sont indépendants de l'implémentation de Board.
- Board est représenté par une liste de k (le nombre de couleurs) bytearrays.
- Le i-ème bytearray à la position n vaut True si et seulement si n est de couleur i.

## À faire dans un premier temps:
- Certaines méthodes doivent être passées dans la classe Board.
- Écrire des tests et ajouter des commentaires.
- Implémenter fillEndCol.

## Possibilités d'amélioration (accélération du programme):
- Compilation just in time avec numba.
- Éviter les copies dans RWS.

## À faire dans un second temps
- Faire une interface en ligne de commande
- Implémenter l'algorithme abstractSimulation.
- Éventuellement tester une autre implémentation de Board.
