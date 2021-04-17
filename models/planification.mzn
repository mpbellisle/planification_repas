include "../data/data_recettes.dzn";
include "../data/parametres.dzn";

int: nb_ingredients;
int: nb_recettes;
int: nb_moments;
int: nb_nationalites;
int: nb_jours;
int: nb_repas = nb_jours * 3;

% Recettes possibles
set of int: ingredient = 1..nb_ingredients;
set of int: recette = 1..nb_recettes;
set of int: moment = 1..nb_moments;
set of int: nationalite = 1..nb_nationalites;
set of int: repas = 1..nb_repas;

array[recette, ingredient] of int: ingredients;
array[recette, moment] of int: moments;
array[recette, nationalite] of int: nationalites;
array[ingredient] of int: qtes_disponibles;
array[ingredient] of int: peremptions;
array[nationalite] of int: preferences_nationalites;

% Préparation de la liste de sortie
array[repas] of var 0..nb_recettes: horaire;

% On choisi des recettes correspondantes au moment de la journée
constraint forall (i in repas) (moments[horaire[i], i mod 3 + 1] == 1 \/ horaire[i] == 0);

% On se limite à la quantité d'ingrédients disponible
constraint forall(i in ingredient) (sum([if horaire[j] > 0 then ingredients[horaire[j], i] else 0 endif| j in repas]) <= qtes_disponibles[i]);

% On respecte les péremptions d'ingrédients
constraint forall(i in ingredient, j in repas) (if horaire[j] > 0 then if ingredients[horaire[j], i] > 0 then j <= peremptions[i] else true endif else true endif);

% On cherche à minimiser le nombre de 0
var 0..nb_repas: nb_zeros;
nb_zeros = sum([horaire[i] == 0| i in repas]);

% Et à maximiser les préférences de nationalités
var float: respect_preferences_nationalites;
respect_preferences_nationalites = sum([if nationalites[i, j] == 1 then preferences_nationalites[j] else 0 endif | i in repas, j in nationalite]);

var float: score;
score = -nb_zeros + respect_preferences_nationalites;

solve maximize score;
