include "../data/data_recettes_out_2000.dzn";
include "../data/parametres.dzn";
include "alldifferent.mzn";

int: nb_ingredients;
int: nb_recettes;
int: nb_moments;
int: nb_nationalites;
int: nb_jours;
int: nb_max_utilisation_recette;
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

% changer les 3 pour nb_moments
% On choisi des recettes correspondantes au moment de la journée
constraint forall (i in repas) (moments[horaire[i], (i-1) mod 3 + 1] == 1 \/ horaire[i] == 0);

% On se limite à la quantité d'ingrédients disponible
constraint forall(i in ingredient) (sum([if horaire[j] > 0 then ingredients[horaire[j], i] else 0 endif| j in repas]) <= qtes_disponibles[i]);

% On respecte les péremptions d'ingrédients
constraint forall(i in ingredient, j in repas) (if horaire[j] > 0 then if ingredients[horaire[j], i] > 0 then j div nb_moments <= peremptions[i] else true endif else true endif);

% Toutes les recettes sont différentes
constraint forall(i in recette) (sum([horaire[j] == i |j in repas]) <= nb_max_utilisation_recette);

% Planifier plus tôt que tard
constraint forall(i in 1..nb_repas-nb_moments) ((horaire[i] == 0 /\ horaire[i+3] == 0) \/ horaire[i] != 0);

% Céduler les recettes en ordre de péremptions pour briser des symmétries
array[recette] of var int: peremptions_recettes;
constraint forall (i in recette)
(
  let {
  array[ingredient] of var int: peremptions_recettes_ingredients;
  } in
  forall(j in ingredient) ((peremptions_recettes_ingredients[j] == if ingredients[i, j] == 1 then peremptions[j] else 10000 endif) /\
  peremptions_recettes[i] = min(peremptions_recettes_ingredients))
);
constraint forall(i in 1..nb_repas-3) (if horaire[i] > 0 /\ horaire[i+3] > 0 then peremptions_recettes[horaire[i]] <= peremptions_recettes[horaire[i+nb_moments]] endif);

% On cherche à minimiser le nombre de 0
var 0..nb_repas: nb_zeros;
nb_zeros = sum([horaire[i] == 0| i in repas]);

% Et à maximiser les préférences de nationalités
var int: respect_preferences_nationalites;
respect_preferences_nationalites = sum([if horaire[i] > 0 then if nationalites[horaire[i], j] == 1 then preferences_nationalites[j] else 0 endif else 0 endif | i in repas, j in nationalite]);

var int: score;
score = -nb_zeros * 10 + respect_preferences_nationalites;

solve maximize score;
