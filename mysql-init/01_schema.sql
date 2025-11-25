CREATE DATABASE IF NOT EXISTS life_rpg
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE life_rpg;

-- 1) Répertoire des Quêtes
CREATE TABLE IF NOT EXISTS quests (
  id INT AUTO_INCREMENT PRIMARY KEY,

  nom_arc VARCHAR(255),
  arc VARCHAR(255),
  frequence VARCHAR(50),
  quete TEXT,
  xp_par_quete INT,
  intensite INT,
  rep_niveau INT NULL,
  repetition INT,
  statut TINYINT(1),
  type_bareme INT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2) Barème XP
-- Clé / XP Intensité 1 / XP Intensité 2 / XP Intensité 3
CREATE TABLE IF NOT EXISTS xp_lookup (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cle VARCHAR(50),
  xp_intensite_1 INT,
  xp_intensite_2 INT,
  xp_intensite_3 INT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3) Progression des niveaux
-- Noms_Niveaux / Paliers_Progressifs / Paliers_Lineaires
CREATE TABLE IF NOT EXISTS level_progression (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom_niveau VARCHAR(50),
  palier_progressif DECIMAL(6,3),
  palier_lineaire DECIMAL(6,3)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 4) Joueur
-- Nom / Niveau / XP Actuelle / Date de Début / Type Progression /
-- XP Objectif Total / Durée du Jeu (Années) / XP Palier Actuel (Absolu) /
-- XP Palier Suivant (Absolu) / AvatarURL
CREATE TABLE IF NOT EXISTS players (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  niveau VARCHAR(50),
  xp_actuelle INT,
  date_debut DATE,
  type_progression VARCHAR(50),
  xp_objectif_total INT,
  duree_jeu_annees INT,
  xp_palier_actuel INT,
  xp_palier_suivant INT,
  avatar_url TEXT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 5) Arcs narratifs
-- ID Arc / Nom Modifiable / Description
CREATE TABLE IF NOT EXISTS arcs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_arc VARCHAR(50),
  nom_modifiable VARCHAR(255),
  description TEXT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 6) Paliers (Sanctuaire des Paliers)
-- Arc Associé / Description / Difficulté / XP Obtenue (Fixe) / Atteint?
CREATE TABLE IF NOT EXISTS milestones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  arc_associe VARCHAR(255),
  description TEXT,
  difficulte VARCHAR(50),
  xp_obtenue INT,
  atteint TINYINT(1)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
