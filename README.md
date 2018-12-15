# Le fantôme de l'opéra

## Introduction

Ce projet contient les sources de nos intelligences artificielles entrainées spécialement à jouer au jeu de plateau, le fantôme de l'opéra.

C'est un jeu à 2 joueurs, un fantôme et un inspecteur. Le but du fantôme est de faire fuir la castafiore de l'opéra pour annuler la représentation, et le but de l'inspecteur est de démasquer le fantôme avant que la castafiore ne décide de s'en aller.

Le fantôme fera se rapprocher un peu plus la castafiore de la sortie pour chaque personne encore suspecte à la fin du tour.

L'inspecteur innocentera des gens petit à petit pour démasquer le fantôme.

Nous vous proposons alors 2 intelligences artificielles pouvant spécialement entrainées à jouer l'inspecteur et le fantôme.

## Les IA monsterpiece

Nos IA font toute les deux partie du type d'IA Monsterpiece, qui sont à la fois des monstres et des chef d'oeuvre #FrankEinstein.

Ce type d'IA a été spécifiquement conçu pour ce jeu. Il s'agit d'une intelligence entrainée par renforcement selon la méthode de deep learning des qvalues.

Le principe est simple, nous représentons le plateau de jeu selon plusieurs paramètres et, par un apprentissage par l'expérience, nous entrainons l'IA à reconnaître une situation favorable d'une situation défavorable en lui attribuant des récompenses et des punitions.

A chaque tour, une IA regardera l'arbre des possibilités s'ouvrant à elle et, grâce à son expérience, choisira le coup qui lui permettra d'arriver dans la meilleur disposition pour gagner.

Nous avons réalisé des sessions d'entrainement contre des IA ne prenant que des décisions aléatoire, donc imprévisibles.

Nos résultats sont d'un taux de victoire de 75% pour l'inspecteur et de 60% pour le fantôme.

Etant donné que les règles sont sont légèrement favorable à l'inspecteur du fait du processus très rapide d'innocentement, il est naturellement plus performant.

Ce qui est très important avec ce type d'intelligence artificielle est qu'elle doit avoir une connaissance précise du plateau au moment ou elle joue afin de calculer les bons coups pour prendre la meilleure décision.

## Lancer l'IA dans le jeu

Pour exécuter l'IA vous pouvez utiliser le script `fantome_opera_serveur.py`.

Les IA de l'inspecteur et du fantôme sont configurées en bas sur les lignes :

```python
Thread(target=inspector.lancer).start()
Thread(target=ghost.lancer).start()
```
 
Pour lancer une IA aléatoire contre l'un ou l'autre, vous avez accès au module `dummy`.

Pour lancer le fantôme contre l'IA aléatoire, remplacez-les par :

```python
Thread(target=dummy.lancer_inspector).start()
Thread(target=ghost.lancer).start()
```

Pour lancer l'inspecteur contre l'IA aléatoire, remplacez-les par :

```python
Thread(target=inspector.lancer).start()
Thread(target=dummy.lancer_ghost).start()
```

## Le bonus

En bonus, nous avons également un projet Unity qui nous permet de visualiser le déroulement d'une partie une fois celle-ci terminée afin d'évaluer les performances des IA.

