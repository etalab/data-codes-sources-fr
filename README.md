[![CircleCI build status](https://img.shields.io/circleci/project/github/AntoineAugusti/data-codes-sources-fr.svg?style=flat-square)](https://circleci.com/gh/AntoineAugusti/data-codes-sources-fr)
[![Software License](https://img.shields.io/badge/License-MIT-orange.svg?style=flat-square)](https://github.com/AntoineAugusti/data-codes-sources-fr/blob/master/LICENSE.md)
[![goodtables.io](https://goodtables.io/badge/github/AntoineAugusti/data-codes-sources-fr.svg)](https://goodtables.io/github/AntoineAugusti/data-codes-sources-fr)

# Données Codes Sources France
Récupère des métadonnées sur les dépôts de code publiés par les comptes d’organisation d’organismes publics en France.

La liste des comptes est donnée par [la liste de la DINSIC](https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/OrgAccounts) et la liste des organisations sur [government.github.com](https://raw.githubusercontent.com/github/government.github.com/gh-pages/_data/governments.yml).

Seules les données des organisations sur GitHub sont récupérées.

## Déploiement et hébergement
Les données sont mises à jour deux fois par heure [grâce à CircleCI](https://circleci.com/gh/AntoineAugusti/data-codes-sources-fr).

## Description des données

## Métadonnées d'un répertoire Git
Ces fichiers se trouvent dans le répertoire `data/repertoires`.

### Modèle de données
- Clé primaire : `repertoire_url`

#### `nom`

- Description : Le nom du répertoire
- Type : chaîne de caractères

#### `organisation_nom`

- Description : Le nom de l'organisation
- Type : chaîne de caractères

#### `plateforme`

- Description : La plateforme de dépôt de code
- Type : chaîne de caractères
- Valeurs autorisées : GitHub

#### `repertoire_url`

- Description : L'URL vers le répertoire
- Type : chaîne de caractères (format `uri`)

#### `description`

- Description : La description du répertoire
- Type : chaîne de caractères

#### `est_fork`

- Description : Indique si le répertoire est un fork
- Type : booléen

#### `date_creation`

- Description : La date de création du répertoire
- Type : date et heure

#### `derniere_mise_a_jour`

- Description : La date de dernière mise à jour du répertoire
- Type : date et heure

#### `homepage`

- Description : URL vers la page d'accueil du projet
- Type : chaîne de caractères

#### `nombre_stars`

- Description : Le nombre de fois où le répertoire a été ajouté aux favoris
- Type : nombre entier
- Valeur minimale : 0

#### `nombre_forks`

- Description : Le nombre de fois où le répertoire a été forké
- Type : nombre entier
- Valeur minimale : 0

#### `licence`

- Description : La licence du répertoire, telle que détectée par la plateforme
- Type : chaîne de caractères

#### `nombre_issues_ouvertes`

- Description : Le nombre d'issues actuellement ouvertes
- Type : nombre entier

#### `langage`

- Description : Le langage principal du répertoire, tel que détecté par la plateforme
- Type : chaîne de caractères

#### `topics`

- Description : Les tags du répertoire
- Type : chaîne de caractères

## Métadonnées d'une organisation Git
Ces fichiers se trouvent dans le répertoire `data/organisations`.


### Modèle de données
- Clé primaire : `login`

#### `login`

- Description : Le pseudo de l'organisation
- Type : chaîne de caractères
- Exemple : Etalab

#### `description`

- Description : La description de l'organisation
- Type : chaîne de caractères
- Exemple : Observatoire accidentologie plaisance et loisirs nautiques France

#### `nom`

- Description : Le nom complet de l'organisation
- Type : chaîne de caractères
- Exemple : Ministère de l'Intérieur

#### `organisation_url`

- Description : URL vers l'organisation
- Type : chaîne de caractères (format `uri`)
- Exemple : https://github.com/etalab

#### `site_web`

- Description : Site web de l'organisation
- Type : chaîne de caractères
- Exemple : https://etalab.gouv.fr

#### `adresse`

- Description : Adresse physique de l'organisation
- Type : chaîne de caractères
- Exemple : Paris, France

#### `email`

- Description : Adresse e-mail de contact de l'organisation
- Type : chaîne de caractères (format `email`)
- Exemple : contact@etalab.gouv.fr

#### `est_verifiee`

- Description : Indique si l'organisation a prouvé qu'elle détenait les noms de domaines associés à son organisation
- Type : booléen
- Exemple : true

#### `nombre_repertoires`

- Description : Le nombre de répertoires publics de l'organisation
- Type : nombre entier
- Exemple : 42
- Valeur minimale : 0

#### `date_creation`

- Description : La date de création de l'organisation
- Type : date et heure
- Exemple : 2013-08-26T16:03:40Z

#### `plateforme`

- Description : La plateforme utilisée de l'organisation
- Type : chaîne de caractères
- Exemple : GitHub
- Valeurs autorisées : GitHub

## Licence
MIT
