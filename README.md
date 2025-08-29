# BlenderAscGridToMesh

Convertir plusieurs tuiles **ASCII Grid (.asc)** de terrain en un seul maillage 3D dans **Blender**.

Le script lit chaque tuile d'élévation, crée un maillage décimé pour chacune, puis les fusionne en une surface continue. Conçu principalement pour les données RGE ALTI® (IGN France), mais adaptable à tout format ASCII Grid.

## Fonctionnalités

- Charger plusieurs tuiles `.asc` depuis un dossier
- Rééchantillonner les données d'élévation via un facteur de décimation configurable
- Fusion automatique des tuiles adjacentes avec remplissage des faces manquantes
- Production d'un unique objet Blender représentant le terrain complet

## Prérequis

- **Blender** (2.8+ recommandé) avec accès à Python
- Des fichiers ASCII Grid (.asc) contenant des données d'altitude
- Connaissances de base de la console Python ou de l'éditeur de scripts de Blender

## Installation & Configuration

1. Cloner ou télécharger ce dépôt dans un emplacement accessible à Blender
2. Placer vos fichiers `.asc` dans un dossier dédié (ex. `data/`)
3. Ouvrir Blender et passer à l'espace de travail **Scripting**
4. Dans l'éditeur de texte, charger le fichier `import_asc.py`

## Utilisation

1. **Modifier la variable `folder`** en haut du fichier `import_asc.py` pour pointer vers le dossier contenant vos fichiers `.asc` :

```python
folder = "/chemin/absolu/vers/vos/fichiers/asc"
```

2. **Ajuster `invert_res`** pour changer le facteur de décimation (ex. `invert_res = 59`)

3. **Exécuter le script** (bouton « Run Script » ou `Alt+P`)

4. Après traitement, un nouvel objet maillé représentant toutes les tuiles fusionnées apparaîtra dans la scène

> **💡 Astuce :** Le script lit les fichiers dans l'ordre alphabétique inversé, puis fusionne chaque tuile avec la précédente. Assurez-vous que les noms de fichiers se trient alphabétiquement selon l'agencement spatial souhaité.

## Comment ça marche

- **Analyse de l'en-tête :** chaque fichier `.asc` est lu pour extraire les métadonnées (dimensions, taille de cellule, valeur « nodata », etc.)
- **Création des sommets :** les altitudes sont converties en sommets via `bmesh`, en appliquant le facteur de décimation pour réduire la densité de points
- **Génération des faces :** des quadrilatères sont créés à partir des sommets, formant le maillage de chaque tuile
- **Assemblage des tuiles :** les sommets de bord sont mémorisés pour relier les tuiles adjacentes et combler les éventuels vides

## Exemple

Le `README.md` de ce dépôt (ce fichier) inclut une capture de référence. Pour obtenir un résultat similaire, téléchargez plusieurs tuiles RGE ALTI® depuis l'IGN, placez-les dans votre `folder`, puis lancez `import_asc.py`.

## Personnalisation

- **Échelle :** actuellement, les coordonnées sont divisées par 1000 (pour passer des mètres aux kilomètres). Modifiez `create_verts` si vous souhaitez une autre échelle
- **Options de sortie :** une fois le maillage généré, vous pouvez lui appliquer des matériaux, des modificateurs, ou l'exporter vers d'autres formats avec les outils standard de Blender

## Structure du code

Le script principal `import_asc.py` contient :

### Variables globales
- `folder` : chemin vers les fichiers .asc
- `invert_res` : facteur de décimation des données
- `infos` : métadonnées du fichier en cours
- `meshes` : données de connexion entre tuiles

### Fonctions principales
- `get_variable()` : analyse l'en-tête des fichiers .asc
- `create_verts()` : génère les sommets du maillage
- `create_faces()` : crée les faces quadrilatères
- `create_object()` : traite un fichier .asc complet
- `create_missing_faces()` : connecte les tuiles adjacentes

## Remerciements

- **IGN France** pour les jeux de données RGE ALTI®
- Les modules Blender `bpy` et `bmesh` pour la génération de maillage

## Licence

Ce projet est fourni tel quel, sans garantie. Référez-vous à la licence du dépôt (si présente) ou adaptez le script pour un usage personnel.