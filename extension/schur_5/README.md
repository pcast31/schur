- Décompresser all_partitions.7z (environ 2.6GB) et le mettre dans le dossier partitions.


- all_partitions contient 56.854.400 partitions de 1..160 en 5 sous-ensembles sans somme. Les partitions sont groupées par 10.000 (sauf 2 fichiers qui en contiennent moins).


- Si vous voulez enregistrer des choses dans un fichier sans les mettre sur git, enregistrer les dans le dossier partitions (son contenu est ignoré par git).


- Les partitions sont retournées sous forme d'une liste 5 listes d'entiers rangés par ordre croissant (chaque liste représente un sous-ensemble sans somme). Les sous-ensembles sont ordonnés selon leur minimum (ordre croissant).


- Ne pas faire list(load_partitions) car vous n'aurez pas assez de place dans votre RAM. En effet, le format de retour des partitions est facile à utiliser mais prend beaucoup de place (les partitions dans all_partitions sont stockées sous forme d'entiers en base 5).


- Pour sélectionner N partitions ayant une certaine propriété :
```python
 from load_partitions import select_partitions

 # Valeurs par defaut

 def necessary_condition(partition):
     return True

 def fitness_function(partition):
     return 0

 max_size = 10_000

 partitions = select(necessary_condition, fitness_function, max_size)
```
    - N < 2*10^6 sinon il faut pas mal de RAM.
    - Si necessary_condition = None, sélectionne uniquement en fonction du score.
    - Si fitness_function = None, sélectionne les N premières partitions vérifiant la condition nécessaire donnée.


- Pour itérer sur toutes les partitions :
```python
 from load_partitions import load_partitions

 for partition in load_partitions():
     do_something(partition)
```


- Pour charger un seul fichier :
```python
 from load_partitions import read_file

 for partition in read_file(42):
     do_something(partition)

 # OU

 for partition in read_file("00042"):
     do_something(partition)
```
