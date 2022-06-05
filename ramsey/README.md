# Nouveautés

## Nouveautés théoriques
-   Introduction des ***b-sf-templates*** pour les nombres de Ramsey linéaires : extension aux [templates pour les nombres de Ramsey linéaires](https://arxiv.org/abs/1912.01164) de l'amélioration faite aux S-templates en s'inspirant des b-WS-templates
-   *Raffinement sur la dernière ligne* des b-sf-templates (à la manière de celui pour les WS-templates)

## Nouvelles inégalités
| Couleurs ajoutées | Nos (a, b, c)  | Anciens (a, b) |
| ----------------- | -------------- | -------------- |
| 3 , 3             | 10 , 2 , 0 \*  | 9  , 4         |
| 3 , 4             | 19 , 2 , 0 \*  | 18 , 7         |
| 3 , 5             | 31 , 2 , 1 \** | 30 , 12        |
| 5 , 4             | 55 , 23 , 0    | 51 , 21        |

\* utilise un b-sf-template non exprimable en tant que sf-template  
\*\* utilise en plus le raffinement sur les b-sf-templates

## Nouvelles bornes inférieures
-   R(3 , 4 , 5 , 5) ≥ 764 (ancienne borne : 729)
-   Amélioration des bornes inférieures pour certains R<sub>r</sub>(3) (via les bornes induites pour les nombres de Schur)
-   Probablement d'autres bornes : il existe une multitude d'inégalités et de constructions pour les nombres de Ramsey, il faudrait donc les recenser puis calculer les bornes induites afin de voir quelles bornes pour les nombres de Ramsey ont été améliorés ; R(3 , 4 , 5 , 5) est le seul nombre de Ramsey dont l'ancienne borne inférerieur était citée explicitement et pour lequel les nouvelles inégalités conduisent à une amélioration.



# Pistes
Je pense qu'il est possible de rechercher des templates afin d'ajouter (5, 5) et (4, 4, 4) avec des hypothèses moins restrictives que celles utilisées dans [\[Rowley, Improved Lower Bounds for Multicolour Ramsey Numbers using SAT-Solvers\]](https://arxiv.org/abs/2203.13476). Ces deux cas sont pertinents car ils concernent les nombres de Ramsey R<sub>r</sub>(n) qui sont les plus étudiés et peuvent éventuellement améliorer la borne sur leur taux de croissance assymptotique en plus de donner des bornes inférieures pour les petites valeurs.



# Graphes

-   stockés dans results/graphs/
-   R(k<sub>1</sub> , ... , k<sub>r</sub> ; n).npy matrice d'adjacence d'un coloriage avec :
    -   n la taille du graphe complet
    -   r le nombre de couleurs
    -   k<sub>i</sub> le plus petit entier tel que la couleur i ne contienne pas de clique (i.e. de sous-graphe complet) de taille k<sub>i</sub>
-   R(k<sub>1</sub> , ... , k<sub>r</sub> ; n).npy prouve R(k<sub>1</sub> , ... , k<sub>r</sub>) ≥ n + 1



# Partitions

-   stockées dans results/partitions/
-   U(k<sub>1</sub> , ... , k<sub>r</sub> ; n).txt coloriage avec :
    -   n la taille de la partition
    -   /!\\ conduit à un graphe de taille n + 1
    -   r le nombre de couleurs
    -   k<sub>i</sub> le plus petit entier tel que la couleur i ne contienne pas un sous-ensemble S de taille k<sub>i</sub> - 1 vérifiant : pour tout x, y dans S, |x - y| est de couleur i
-   U(k<sub>1</sub> , ... , k<sub>r</sub> ; n).txt prouve R(k<sub>1</sub> , ... , k<sub>r</sub>) ≥ n + 2 [\[Abbott & Hanson, A problem of Schur and its generalizations\]](https://www.semanticscholar.org/paper/A-problem-of-Schur-and-its-generalizations-Abbott-Hanson/825cd3ad083d1bfe12aca9b7cff838c542e979b5)



# Templates

-   stockés dans results/templates/
-   L(k<sub>1</sub> , ... , t , ... , k<sub>r</sub> ; a\[-b\]\[-c\]).txt coloriage avec :
    -   a la largeur du template
    -   si ni b ni c n'est précisé, c'est un sf-template et b existe et vérifie 1 ≤ b \< a
    -   si b est précisé, c'est un b-sf-template
    -   l'existence éventuelle de c correspond à l'équivalent du raffinement sur la dernière ligne des WS-templates utilisé notamment pour obtenir WS(n + 3) ≥ 42 * S(n) + 24 en utilisant un 23-WS-template de largeur 42
    -   k<sub>i</sub> le plus petit entier tel que la couleur i <u>après construction</u> ne contienne pas un sous-ensemble S de taille k<sub>i</sub> - 1 vérifiant : pour tout x, y dans S, |x - y| est de couleur i
    -   t la couleur spéciale du template
-   L(k<sub>1</sub> , ... , t , ... , k<sub>r</sub> ; a\[-b\]\[-c\]).txt prouve que U(k<sub>1</sub> , ... , k<sub>r</sub> , k<sub>r+1</sub> , ... , k<sub>r+p</sub>) - 2 ≥ a * (U(k<sub>1</sub> , ... , k<sub>p</sub>) - 2) + b + c
