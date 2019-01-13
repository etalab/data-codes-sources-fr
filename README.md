[![CircleCI build status](https://img.shields.io/circleci/project/github/AntoineAugusti/data-codes-sources-fr.svg?style=flat-square)](https://circleci.com/gh/AntoineAugusti/data-codes-sources-fr)
[![Software License](https://img.shields.io/badge/License-MIT-orange.svg?style=flat-square)](https://github.com/AntoineAugusti/data-codes-sources-fr/blob/master/LICENSE.md)
[![goodtables.io](https://goodtables.io/badge/github/AntoineAugusti/data-codes-sources-fr.svg)](https://goodtables.io/github/AntoineAugusti/data-codes-sources-fr)

# Données Codes Sources France
Récupère des métadonnées sur les dépôts de code publiés par les comptes d’organisation d’organismes publics en France.

La liste des comptes est donnée par [la liste de la DINSIC](https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/OrgAccounts) et la liste des organisations sur [government.github.com](https://raw.githubusercontent.com/github/government.github.com/gh-pages/_data/governments.yml).

Seules les données des organisations sur GitHub sont récupérées.

## Déploiement et hébergement
Les données sont mises à jour régulièrement [grâce à CircleCI](https://circleci.com/gh/AntoineAugusti/data-codes-sources-fr).

## Données
Les données sont publiées aux formats CSV et JSON dans le dossier [data](data). Chaque dossier contient un fichier `all.{csv,json}` qui contient l'ensemble des répertoires ou des organisations. Ces fichiers sont à privilégier lorsque vous souhaitez faire une analyse globale.

## Description des données

### Métadonnées d'un répertoire Git

#### Modèle de données
- Clé primaire : `repertoire_url`

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|nom|chaîne de caractères|Le nom du répertoire|nom-repertoire|Valeur obligatoire|
|organisation_nom|chaîne de caractères|Le nom de l'organisation|etalab|Valeur obligatoire|
|plateforme|chaîne de caractères|La plateforme de dépôt de code|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub|
|repertoire_url|chaîne de caractères (format `uri`)|L'URL vers le répertoire|https://github.com/etalab/nom-repertoire|Valeur obligatoire|
|description|chaîne de caractères|La description du répertoire|Ce répertoire est utile|Valeur optionnelle|
|est_fork|booléen|Indique si le répertoire est un fork|false|Valeur obligatoire|
|date_creation|date et heure|La date de création du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|derniere_mise_a_jour|date et heure|La date de dernière mise à jour du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|homepage|chaîne de caractères|URL vers la page d'accueil du projet|https://etalab.gouv.fr|Valeur optionnelle|
|nombre_stars|nombre entier|Le nombre de fois où le répertoire a été ajouté aux favoris|42|Valeur obligatoire, Valeur minimale : 0|
|nombre_forks|nombre entier|Le nombre de fois où le répertoire a été forké|13|Valeur obligatoire, Valeur minimale : 0|
|licence|chaîne de caractères|La licence du répertoire, telle que détectée par la plateforme|MIT|Valeur optionnelle|
|nombre_issues_ouvertes|nombre entier|Le nombre d'issues actuellement ouvertes|0|Valeur obligatoire, Valeur minimale : 0|
|langage|chaîne de caractères|Le langage principal du répertoire, tel que détecté par la plateforme|Python|Valeur optionnelle|
|topics|chaîne de caractères|Les tags du répertoire|utile,france,opendata|Valeur optionnelle|

### Métadonnées d'une organisation Git

#### Modèle de données
- Clé primaire : `login`

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|login|chaîne de caractères|Le pseudo de l'organisation|Etalab|Valeur obligatoire|
|description|chaîne de caractères|La description de l'organisation|Observatoire accidentologie plaisance et loisirs nautiques France|Valeur optionnelle|
|nom|chaîne de caractères|Le nom complet de l'organisation|Ministère de l'Intérieur|Valeur optionnelle|
|organisation_url|chaîne de caractères (format `uri`)|URL vers l'organisation|https://github.com/etalab|Valeur obligatoire|
|site_web|chaîne de caractères|Site web de l'organisation|https://etalab.gouv.fr|Valeur optionnelle|
|adresse|chaîne de caractères|Adresse physique de l'organisation|Paris, France|Valeur optionnelle|
|email|chaîne de caractères (format `email`)|Adresse e-mail de contact de l'organisation|contact@etalab.gouv.fr|Valeur optionnelle|
|est_verifiee|booléen|Indique si l'organisation a prouvé qu'elle détenait les noms de domaines associés à son organisation|true|Valeur obligatoire|
|nombre_repertoires|nombre entier|Le nombre de répertoires publics de l'organisation|42|Valeur obligatoire, Valeur minimale : 0|
|date_creation|date et heure|La date de création de l'organisation|2013-08-26T16:03:40Z|Valeur obligatoire|
|plateforme|chaîne de caractères|La plateforme utilisée de l'organisation|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub|

## Licence
MIT
