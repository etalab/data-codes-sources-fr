[![CircleCI build status](https://img.shields.io/circleci/project/github/etalab/data-codes-sources-fr.svg?style=flat-square)](https://circleci.com/gh/etalab/data-codes-sources-fr)
[![Software License](https://img.shields.io/badge/Licence-MIT%2C%20Licence%20Ouverte-orange.svg?style=flat-square)](https://github.com/etalab/data-codes-sources-fr/blob/master/LICENSE.md)
[![goodtables.io](https://goodtables.io/badge/github/etalab/data-codes-sources-fr.svg)](https://goodtables.io/github/etalab/data-codes-sources-fr)

# But du dépôt

Le but de ce dépôt est de :
- collecter des métadonnées concernant les dépôts publiés par les comptes d'organisation d'organismes publics ;
- donner de la visibilité à l'ensemble de ces comptes.

Ne sont pour l'instant traités que les comptes présents sur GitHub. Les comptes présents sur d'autres plates-formes (par exemple GitLab) pourront être intégrés dans un second temps.

Pour ajouter le compte d'organisation de votre organisme, vous pouvez proposer de modifier [le fichier](https://github.com/DISIC/politique-de-contribution-open-source/blob/master/comptes-organismes-publics) pertinent dans le dépôt de la DINSIC relatif à la Politique de Contribution Open Source de l'État.

## Déploiement et hébergement
Les données sont mises à jour régulièrement [grâce à CircleCI](https://circleci.com/gh/etalab/data-codes-sources-fr).

## Données
Les données sont publiées aux formats CSV et JSON dans le dossier [data](data). Chaque dossier contient un fichier `all.{csv,json}` qui contient l'ensemble des répertoires ou des organisations. Ces fichiers sont à privilégier lorsque vous souhaitez faire une analyse globale.

## Description des données
Les données sont décrites à l'aide de fichiers [Table Schema](https://frictionlessdata.io/specs/table-schema/) dans [le dossier schemas](./schemas/)

### Métadonnées d'un répertoire Git

#### Modèle de données
- Clé primaire : `repertoire_url`, `organisation_nom`

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|nom|chaîne de caractères|Le nom du répertoire|nom-repertoire|Valeur obligatoire|
|organisation_nom|chaîne de caractères|Le nom de l'organisation|etalab|Valeur obligatoire|
|plateforme|chaîne de caractères|La plateforme de dépôt de code|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub,GitLab|
|repertoire_url|chaîne de caractères (format `uri`)|L'URL vers le répertoire|https://github.com/etalab/nom-repertoire|Valeur obligatoire|
|description|chaîne de caractères|La description du répertoire|Ce répertoire est utile|Valeur optionnelle|
|est_fork|booléen|Indique si le répertoire est un fork|false|Valeur obligatoire|
|est_archive|booléen|Indique si le répertoire est archivé, c'est-à-dire qu'il est en lecture seule|false|Valeur obligatoire|
|date_creation|date et heure|La date de création du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|derniere_mise_a_jour|date et heure|La date de dernière mise à jour du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|page_accueil|chaîne de caractères|URL vers la page d'accueil du projet|https://etalab.gouv.fr|Valeur optionnelle|
|nombre_stars|nombre entier|Le nombre de fois où le répertoire a été ajouté aux favoris|42|Valeur obligatoire, Valeur minimale : 0|
|nombre_forks|nombre entier|Le nombre de fois où le répertoire a été forké|13|Valeur obligatoire, Valeur minimale : 0|
|licence|chaîne de caractères|La licence du répertoire, telle que détectée par la plateforme|MIT|Valeur optionnelle|
|nombre_issues_ouvertes|nombre entier|Le nombre d'issues actuellement ouvertes|0|Valeur obligatoire, Valeur minimale : 0|
|langage|chaîne de caractères|Le langage principal du répertoire, tel que détecté par la plateforme|Python|Valeur optionnelle|
|topics|chaîne de caractères|Les tags du répertoire|utile,france,opendata|Valeur optionnelle|
|software_heritage_exists|booléen|Indique si le répertoire a déjà été archivé sur Software Heritage|false|Valeur obligatoire|
|software_heritage_url|chaîne de caractères (format `uri`)|L'URL vers l'interface web de Software Heritage pour ce répertoire|https://archive.softwareheritage.org/browse/origin/https://github.com/etalab/etalab/directory/|Valeur obligatoire|

### Métadonnées d'une organisation Git

#### Modèle de données
- Clé primaire : `login`

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|login|chaîne de caractères|Le pseudo de l'organisation|Etalab|Valeur obligatoire|
|description|chaîne de caractères|La description de l'organisation|Observatoire accidentologie plaisance et loisirs nautiques France|Valeur optionnelle|
|nom|chaîne de caractères|Le nom complet de l'organisation|Ministère de l'Intérieur|Valeur optionnelle|
|organisation_url|chaîne de caractères (format `uri`)|URL vers l'organisation|https://github.com/etalab|Valeur obligatoire|
|site_web|chaîne de caractères (format `uri`)|Site web de l'organisation|https://etalab.gouv.fr|Valeur optionnelle|
|adresse|chaîne de caractères|Adresse physique de l'organisation|Paris, France|Valeur optionnelle|
|email|chaîne de caractères (format `email`)|Adresse e-mail de contact de l'organisation|contact@etalab.gouv.fr|Valeur optionnelle|
|est_verifiee|booléen|Indique si l'organisation a prouvé qu'elle détenait les noms de domaines associés à son organisation|true|Valeur optionnelle|
|nombre_repertoires|nombre entier|Le nombre de répertoires publics de l'organisation|42|Valeur obligatoire, Valeur minimale : 0|
|date_creation|date et heure|La date de création de l'organisation|2013-08-26T16:03:40Z|Valeur optionnelle|
|plateforme|chaîne de caractères|La plateforme utilisée de l'organisation|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub,GitLab|

# Droits d’auteur et licence
Le code source du répertoire est publié sous [la licence MIT](LICENSE.md). Les données, disponibles dans le répertoire [data](data) sont publiées sous la [Licence Ouverte 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence).

© 2018-2020 Direction interministérielle du numérique et du système d’information et de communication de l’État, Antoine Augusti, Bastien Guerry.

© 2018-2020 Les autres contributeurs dans la liste est accessible via l’historique du dépôt.
