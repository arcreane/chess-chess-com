[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ChwpCt9g)
<<<<<<< HEAD
Dimension : 600 x 400
# ♟ Jeu d'Échecs — Projet 2025-2026
 
Projet de jeu d'échecs en Python, développé dans le cadre du module de Programmation Orientée Objet.
 
> **Équipe :** Iwan Hosny · Adrien Berthoux · Noah Catheland · Noam Sakly
 
---
 
## 📁 Structure du projet
 
```
chess-project/
├── main.py                  # point d'entrée du jeu
├── requirements.txt         # dépendances (Pygame)
├── README.md
├── .gitignore
│
├── src/                     # code source
│   ├── __init__.py
│   ├── position.py          # classe Position (case du plateau)
│   ├── piece.py             # classe abstraite Piece + constantes WHITE/BLACK
│   ├── pieces.py            # King, Queen, Rook, Bishop, Knight, Pawn
│   ├── board.py             # plateau de jeu
│   ├── player.py            # Player (humain) + AIPlayer
│   ├── chess_game.py        # orchestration de la partie
│   └── save.py              # sauvegarde / restauration JSON
│
├── tests/                   # tests unitaires (unittest)
│   ├── test_position.py
│   ├── test_board.py
│   └── test_save.py
│
└── saves/                   # parties sauvegardées (.json)
```
 
---
 
## 🚀 Lancer le jeu
 
### Mode texte (par défaut)
 
```bash
python main.py
```
 
### Contre l'IA aléatoire
 
```bash
python main.py --ai
```
 
### Reprendre une partie sauvegardée
 
```bash
python main.py --load ma_partie
```
 
### Commandes pendant une partie
 
| Commande      | Effet                                            |
|---------------|--------------------------------------------------|
| `e2 e4`       | Joue le coup (case source → case destination)    |
| `save <nom>`  | Sauvegarde la partie dans `saves/<nom>.json`     |
| `load <nom>`  | Charge une partie sauvegardée                    |
| `quit`        | Quitte le jeu                                    |
 
---
 
## 🧪 Lancer les tests
 
```bash
python -m unittest discover -s tests -v
```
 
---
 
## 🏗 Architecture (UML)
 
| Classe        | Rôle                                                       |
|---------------|------------------------------------------------------------|
| `Position`    | Représente une case du plateau (colonne + ligne)           |
| `Piece`       | Classe mère abstraite — définit `isValidMove()`            |
| `King` ... `Pawn` | Pièces concrètes implémentant `isValidMove()`          |
| `Board`       | Gère l'état du plateau (dictionnaire de pièces)            |
| `Player`      | Joueur humain (saisit ses coups via `askMove()`)           |
| `AIPlayer`    | Sous-classe de Player générant un coup aléatoire           |
| `Chess`       | Orchestre la partie (boucle de jeu, validation, sauvegarde) |
 
---
 
## 👥 Répartition du travail
 
| Tâche                                | Responsable(s) | État |
|--------------------------------------|----------------|------|
| Classes `Position`, `Piece` (abstract) | Tous (init: Iwan) |  ⏳ |
| Classes `Board` & `Chess` (squelette) | Tous (init: Iwan) |  ⏳ |
| `isValidMove()` — King & Queen        | Adrien         | ⏳ |
| `isValidMove()` — Rook & Bishop       | Noah           | ⏳ |
| `isValidMove()` — Knight & Pawn       | Noam           | ⏳ |
| Interface graphique Pygame            | Noah           | ⏳ |
| Sauvegarde / restauration (fichier)   | Iwan           |  ⏳|
| `isCheckMate()`                       | Adrien         | ⏳ |
| `AIPlayer` (random)                   | Noam           | ⏳ |
| Tests unitaires (UnitTest)            | Tous           |  ⏳|
| Déplacements spéciaux                 | Tous           | ⏳ |
| README & documentation                | Iwan           |  ⏳ |
 
---
 
## 🎯 Améliorations envisagées
 
### Priorité haute
- **Interface graphique Pygame** : sprites, cases surbrillées sur sélection, clic souris
- **Roque** (petit et grand)
- **Promotion du Pion** (auto en Reine ou au choix)
- **Prise en passant**
### Bonus (si le temps)
- IA Minimax (au lieu du mouvement aléatoire)
- Sauvegarde en SQLite
- Horloge d'échecs par joueur
- Historique des coups au format PGN
---
 
## 🛠 Outils de l'équipe
 
- **GitHub** : versionnage (branches par fonctionnalité, commits réguliers)
- **Trello** : suivi des tâches (Backlog → À faire → En cours → À tester → Terminé)
- **Discord / Teams** : communication
- **Moodle** : dépôt des livrables
- **Pygame** : interface graphique
