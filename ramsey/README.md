# explications

Code LaTeX pour amelioration_templates_ramsey_schur.pdf qui contient une description des nouveautés théoriques,  des nouvelles inégalités et des nouvelles bornes inférieures.



# solvers

Placer vos SAT solvers favoris ici.


# src

Divers codes Python pour la recherche de b-templates et la vérification des résultats.


# fast_template

Code Rust (en cours d'écriture) pour génération et la simplification efficaces de formules booléennes encodant l'existence de templates (pas pour les b-templates).


# results

## Graphes
-   stockés dans results/graphs/
-   R(k<sub>1</sub> , ... , k<sub>r</sub> ; n).npy matrice d'adjacence d'un coloriage avec :
    -   n la taille du graphe complet
    -   r le nombre de couleurs
    -   k<sub>i</sub> le plus petit entier tel que la couleur i ne contienne pas de clique (i.e. de sous-graphe complet) de taille k<sub>i</sub>
-   R(k<sub>1</sub> , ... , k<sub>r</sub> ; n).npy prouve R(k<sub>1</sub> , ... , k<sub>r</sub>) ≥ n + 1

## Partitions
-   stockées dans results/partitions/
-   L(k<sub>1</sub> , ... , k<sub>r</sub> ; n).txt coloriage avec :
    -   n la taille de la partition
    -   /!\\ conduit à un graphe de taille n + 1
    -   r le nombre de couleurs
    -   k<sub>i</sub> le plus petit entier tel que la couleur i ne contienne pas un sous-ensemble S de taille k<sub>i</sub> - 1 vérifiant : pour tout x, y dans S, |x - y| est de couleur i
-   L(k<sub>1</sub> , ... , k<sub>r</sub> ; n).txt prouve R(k<sub>1</sub> , ... , k<sub>r</sub>) ≥ n + 2 [\[Abbott & Hanson, A problem of Schur and its generalizations\]](https://www.semanticscholar.org/paper/A-problem-of-Schur-and-its-generalizations-Abbott-Hanson/825cd3ad083d1bfe12aca9b7cff838c542e979b5)

## Templates
-   stockés dans results/templates/
-   T(k<sub>1</sub> , ... , t , ... , k<sub>r</sub> ; a\[-b\]\[-c\]).txt coloriage avec :
    -   a la largeur du template
    -   si b n'est pas précisé, c'est un sf-template, i.e. b = 0
    -   si b est précisé, c'est un b-template
    -   c est la longueur du coloriage final (non précisé dans le cas du coloriage par défaut)
    -   t désigne la couleur template
    -   k<sub>i</sub> le plus petit entier tel que la couleur i <u>après construction</u> ne contienne pas un sous-ensemble S de taille k<sub>i</sub> - 1 vérifiant : pour tout x, y dans S, |x - y| est de couleur i
    -   t la couleur spéciale du template
-   T(k<sub>1</sub> , ... , k<sub>i - 1</sub> , t , k<sub>i + 1</sub> , ... , k<sub>r</sub> ; a\[-b\]\[-c\]).txt prouve que L(k<sub>1</sub> , ... , k<sub>i - 1</sub> , l<sub>1</sub> , k<sub>i + 1</sub> , k<sub>r</sub> , l<sub>2</sub> , ... , l<sub>p</sub>) - 2 ≥ a * (L(l<sub>1</sub> , ... , l<sub>p</sub>) - 2) + b + c
