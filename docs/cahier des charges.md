# Cahier des charges - AutomMixer

## Repository

- Git : git@github.com:mag-yves/automixer.git

## 1. Contexte

AutomMixer est un script destiné à automatiser le montage de vidéos courtes en remplaçant leur piste audio par une intro sonore choisie aléatoirement dans une banque locale.

Le but est de traiter un lot de vidéos déjà préparées, sans intervention manuelle vidéo par vidéo, afin d’obtenir des versions finalisées prêtes à être publiées.

## 2. Sources de données

### 2.1 Source des vidéos

Le dossier source des vidéos est `videosource`.

Sa structure est la suivante :
- un dossier principal, par exemple `d01` ou `2026-06-27_14-34-27-babesByStableYogiSDXL`
- un sous-dossier contenant la vidéo, par exemple `233133_00001`
- les fichiers vidéo sont au format `.mp4`

### 2.2 Source des sons

Le dossier source des sons est `soundsource`.

Il contient plus de 100 fichiers audio au format `.mp3`, générés localement, sans risque de droit d’auteur.

## 3. Objectif du script

Le script doit parcourir le dossier `videosource`, détecter les vidéos à traiter, puis pour chaque vidéo :
- sélectionner aléatoirement un fichier audio depuis `soundsource`
- remplacer la piste audio de la vidéo par ce son
- adapter la durée du son à celle de la vidéo
- tronquer le son si nécessaire lorsque sa durée est supérieure à celle de la vidéo
- enregistrer la vidéo modifiée dans le même dossier
- produire un nom unique, incrémental, pour éviter d’écraser les versions précédentes
- conserver une trace du son utilisé dans un fichier de log

## 4. Règles fonctionnelles

### 4.1 Traitement par lot
Le script doit traiter plusieurs vidéos de manière automatisée sur l’ensemble du dossier source.

### 4.2 Sélection audio
- Le choix du fichier audio doit être aléatoire.
- La sélection doit pouvoir être contrôlée pour éviter des répétitions immédiates du même son dans une suite de traitements.

### 4.3 Durée du son
- La durée de la vidéo sert de référence.
- Si le son est plus long que la vidéo, il est coupé.
- Si le son est plus court, il est utilisé tel quel, ou éventuellement bouclé selon les décisions de développement à valider.

### 4.4 Sortie vidéo
La vidéo de sortie est enregistrée sous le format :
- `<nom d'origine>_snd_<n>.mp4`

Le suffixe `_snd_<n>` porte un numéro incrémental pour permettre plusieurs traitements successifs sans écraser les fichiers déjà générés.

### 4.5 Journalisation
Le script doit ajouter un fichier `<nom_du_sous-dossier>_sound_<n>.txt` dans le dossier traité, avec le même numéro d'itération que la vidéo de sortie.

Ce fichier doit contenir au minimum :
- le nom du fichier audio utilisé
- le nom de la vidéo source
- éventuellement la date et l’heure du traitement

## 5. Exigences de robustesse

Le script doit être conçu pour gérer les cas limites suivants :
- fichiers audio non lisibles
- fichiers vidéo corrompus ou incompatibles
- dossiers vides
- fichiers manquants
- erreurs sur une vidéo sans bloquer le traitement des autres

En cas d’erreur, le script doit continuer le traitement, enregistrer l’information dans les logs et signaler explicitement la cause.

## 6. Développement et validation par phases

Chaque phase doit être validée avant de passer à la suivante.

### Phase 1 - Analyse des sources et validation du périmètre
- vérification de la structure de `videosource` et `soundsource`
- validation des formats acceptés (`.mp4`, `.mp3`)
- identification des cas limites
- définition du comportement en cas d’erreur

### Phase 2 - Prototype de lecture des fichiers
- lecture des dossiers source
- détection des vidéos à traiter
- sélection aléatoire d’un fichier audio
- lecture de la durée de la vidéo et du son

### Phase 3 - Traitement audio et synchronisation
- remplacement de la piste audio
- ajustement du son à la durée de la vidéo
- gestion du tronquage du son
- vérification de la cohérence du rendu audio

### Phase 4 - Export des résultats
- génération du fichier final avec le nom incrémental
- vérification que la sortie est bien enregistrée dans le bon dossier
- contrôle de la validité du fichier produit

### Phase 5 - Journalisation et traçabilité
- création du fichier `<nom_du_sous-dossier>_sound_<n>.txt` avec le numéro d'itération
- enregistrement du son utilisé
- ajout de détails utiles pour le suivi du traitement

### Phase 6 - Validation fonctionnelle
- test sur un petit lot de vidéos
- vérification manuelle du rendu audio et vidéo
- contrôle du nommage incrémental
- validation du comportement sur plusieurs séries de traitement

### Phase 7 - Améliorations et stabilisation
- ajout des garde-fous nécessaires aux cas limites
- optimisation de la robustesse
- documentation des erreurs et des réglages
- préparation du script pour un usage régulier et reproductible

## 7. Améliorations à intégrer

### 7.1 Nommage incrémental des fichiers de sortie
- Le fichier final est enregistré sous le format `<nom d'origine>_snd_<n>.mp4`.
- Le compteur est incrémental pour permettre plusieurs traitements successifs sans écraser les fichiers précédents.
- Le script choisit automatiquement le prochain numéro disponible.

### 7.2 Protection contre l’écrasement
- Les fichiers déjà générés ne doivent pas être remplacés par un nouveau traitement.
- En cas de relance du script, les sorties précédentes restent intactes.

### 7.3 Sélection aléatoire contrôlée
- La sélection du son reste aléatoire, mais peut éviter les répétitions immédiates du même fichier pour un rendu plus varié.

### 7.4 Gestion des erreurs et fichiers non valides
- Les vidéos ou sons illisibles ou corrompus doivent être détectés.
- Le script ignore ces éléments, affiche un message d’erreur dans les logs et continue le traitement des autres fichiers.

### 7.5 Validation de la durée et de la cohérence du rendu
- La durée de la vidéo est la référence.
- Le son est coupé si nécessaire pour respecter cette durée.
- Le script vérifie ensuite que le fichier exporté est bien conforme et exploitable.

### 7.6 Journalisation détaillée
- Le fichier `<nom_du_sous-dossier>_sound_<n>.txt` contient le nom du son utilisé ainsi que, si possible, la date et l’heure du traitement.
- Le script conserve une trace exploitable pour chaque fichier traité.

### 7.7 Log horodaté en terminal par phase de traitement
À chaque étape du traitement, le script doit afficher un message dans le terminal avec horodatage.

Exemple :
- `[2026-08-26 14:30:12] Début du traitement`
- `[2026-08-26 14:30:13] Vidéo détectée : d01/233133_00001/video.mp4`
- `[2026-08-26 14:30:14] Son choisi : intro_42.mp3`
- `[2026-08-26 14:30:15] Son coupé à la durée de la vidéo`
- `[2026-08-26 14:30:16] Sortie enregistrée : video_snd_1.mp4`
- `[2026-08-26 14:30:17] Fichier d01_sound_1.txt mis à jour`

Ces logs permettent de suivre précisément chaque traitement, étape par étape, dans le terminal.

### 7.8 Rapport de traitement global
- Le script fournit un bilan final : nombre de vidéos traitées, nombre d’erreurs et nombre de sorties générées.
- Ce rapport sert à valider le lot traité.

### 7.9 Mode test / dry run
- Un mode de test permet d’exécuter les traitements en simulation sans générer de fichiers finaux.
- Cela permet de vérifier le comportement avant l’exécution réelle.

### 7.10 Paramétrage configurable
- Les chemins `videosource`, `soundsource` et de sortie doivent être paramétrables.
- Il est utile de rendre le suffixe, le mode de sélection du son et le niveau de log configurables.

### 7.11 Vérification du rendu final
- Après export, le script vérifie que le fichier final existe bien et contient un flux audio valide.
- En cas d’anomalie, il signale clairement l’erreur.

## 8. Critères de validation finale

Le projet sera considéré comme validé lorsque :
- toutes les vidéos du dossier source sont détectées correctement
- chaque vidéo reçoit un son sélectionné aléatoirement
- la durée du son est adaptée à celle de la vidéo
- les sorties sont générées avec un nom incrémental unique
- les fichiers précédents ne sont pas écrasés
- un log `<nom_du_sous-dossier>_sound_<n>.txt` est créé pour chaque vidéo traitée
- les erreurs sont signalées sans interrompre le traitement du lot
- les logs terminal sont lisibles et suffisamment détaillés
- le script fonctionne sur plusieurs relances successives sans conflit

## 9. Validation du cahier des charges

Le cahier des charges est considéré comme complet lorsque :
- la structure du projet et les sources sont bien définies
- les règles de traitement sont claires
- les phases de développement sont décrites
- les améliorations acceptées sont intégrées
- les critères de validation finale sont explicités

Une fois ce point validé, le feu-vert est donné pour démarrer le développement.



