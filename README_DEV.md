# BlenderAscGridToMesh

## Présentation

**BlenderAscGridToMesh** est un petit script Python destiné à Blender. Il lit des fichiers ASCII Grid (.asc) contenant un modèle numérique de terrain, puis génère un maillage 3D (mesh) correspondant. Il est pensé pour traiter plusieurs tuiles RGE ALTI® (données IGN françaises) et les fusionner en un seul objet Blender.

[Generated_Mesh.webm](https://github.com/RPSebb/BlenderAscGridToMesh/assets/26611434/03db01fb-813d-4b63-aa76-041da38a2ddb)

## Vue d'ensemble du projet

Ce script permet de :
- Lire des fichiers ASCII Grid (.asc) contenant des données d'altitude
- Convertir automatiquement ces données en maillages 3D dans Blender
- Fusionner plusieurs tuiles de terrain en un objet cohérent
- Optimiser les données par échantillonnage pour des performances optimales

## Structure du dépôt

| Fichier | Rôle principal |
|---------|---------------|
| `import_asc.py` | Script Blender : conversion des fichiers `.asc` en maillages 3D et assemblage des tuiles |

Il n'y a pas d'autres modules ou dépendances ; tout se concentre dans ce script destiné à être exécuté depuis Blender (car il utilise `bpy` et `bmesh`).

## Fonctionnement général

Le script `import_asc.py` suit ce processus :

1. **Lecture d'un dossier** de fichiers `.asc` (`folder`)
2. **Pour chaque fichier** :
   - Lecture de l'en-tête pour récupérer les métadonnées (dimensions, taille de cellule, valeur "no data"…)
   - Création des sommets et des faces pour former une tuile de terrain
   - Stockage des indices des sommets de bord pour pouvoir relier les tuiles entre elles
3. **Fusion** des tuiles successives en un seul objet Blender
4. **Création des faces manquantes** entre les tuiles afin d'obtenir un maillage continu

### Variables globales

Quelques variables globales orientent ce comportement :

- `folder` : chemin vers le répertoire contenant les `.asc`
- `invert_res` : pas d'échantillonnage (ici 59) pour décimer les données
- `infos` : dictionnaire stockant les métadonnées du fichier en cours
- `meshes` : dictionnaire associant chaque tuile à ses sommets de bord

## Détail des fonctions

| Fonction | But et logique |
|----------|---------------|
| `get_variable(line)` | Parse une ligne d'en-tête et met à jour `infos` (ncols, nrows, xllcorner, etc.) |
| `create_verts(y, line, bm)` | À partir d'une ligne de données d'altitude, crée des sommets dans le `bmesh` `bm`. Utilise `invert_res` pour sauter des points et convertit les coordonnées en mètres (échelle 1/1000) |
| `create_faces(bm)` | Génère des quadrilatères à partir des sommets créés, en fonction du nombre de lignes/colonnes effectifs après décimation |
| `get_side_verts(i)` | Calcule les indices de sommets appartenant aux quatre bords de la tuile `i`. Utilisé pour connecter les tuiles adjacentes |
| `get_neighbor(x, y)` | Retourne la structure décrivant les bords d'une tuile voisine (via `meshes`) |
| `create_bottom_face(...)` | Crée des faces reliant une tuile courante à son voisin du dessous |
| `create_left_face(...)` | Crée des faces reliant une tuile courante à son voisin de gauche |
| `create_bottom_left_face(...)` | Crée des faces reliant une tuile courante à son voisin en diagonale bas-gauche |
| `create_missing_faces(obj)` | Parcourt toutes les tuiles enregistrées et complète les faces manquantes entre elles |
| `merge_objects(obj_1, obj_2)` | Fonction utilitaire (non utilisée directement) qui fusionne deux objets Blender via `bpy.ops.object.join()` |
| `create_object(i)` | Lit le fichier `.asc` numéro `i`, construit le mesh correspondant (sommets puis faces) et l'insère dans la scène Blender. Retourne l'objet créé |

## Bloc principal d'exécution

Le script principal :
- Définit le dossier de données et initialise les variables globales
- Lit les fichiers du dossier en ordre inversé
- Crée chaque objet et fusionne progressivement avec le précédent
- Appelle `create_missing_faces` pour relier proprement toutes les tuiles
