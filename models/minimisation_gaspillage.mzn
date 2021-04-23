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
array[nationalite] of float: preferences_nationalites;

% Préparation de la liste de sortie
array[repas] of var 0..nb_recettes: horaire;

% On choisi des recettes correspondantes au moment de la journée
constraint forall (i in repas) (moments[horaire[i], (i-1) mod 3 + 1] == 1 \/ horaire[i] == 0);

% On se limite à la quantité d'ingrédients disponible
constraint forall(i in ingredient) (sum([if horaire[j] > 0 then ingredients[horaire[j], i] else 0 endif| j in repas]) <= qtes_disponibles[i]);

% On respecte les péremptions d'ingrédients
constraint forall(i in ingredient, j in repas) (if horaire[j] > 0 then if ingredients[horaire[j], i] > 0 then j div 3 <= peremptions[i] else true endif else true endif);

% Toutes les recettes sont différentes
constraint forall(i in recette) (sum([horaire[j] == i |j in repas]) <= nb_max_utilisation_recette);

% Planifier plus tôt que tard
constraint forall(i in 1..nb_repas-3) ((horaire[i] == 0 /\ horaire[i+3] == 0) \/ horaire[i] != 0);

% Céduler les recettes en ordre de péremptions pour briser des symmétries
array[recette] of var int: peremptions_recettes;
array[recette] of var int: score_recette_peremptions;
constraint forall (i in recette)
(
  let {
  array[ingredient] of var int: peremptions_recettes_ingredients;
  } in
  forall(j in ingredient) ((peremptions_recettes_ingredients[j] == if ingredients[i, j] == 1 then peremptions[j] else 10000 endif) /\
  peremptions_recettes[i] = min(peremptions_recettes_ingredients))
);
constraint forall(i in 1..nb_repas-3) (if horaire[i] > 0 /\ horaire[i+3] > 0 then peremptions_recettes[horaire[i]] <= peremptions_recettes[horaire[i+3]] endif);

% Calculer le score de péremptions par recette
constraint forall(i in recette) (score_recette_peremptions[i] == sum([100*ingredients[i, j] div max(peremptions[j], 1) | j in ingredient]));

% Et à maximiser l'utilisation des ingrédients périssables
var int: score_peremptions;

score_peremptions = sum([if horaire[i] > 0 then score_recette_peremptions[horaire[i]] else 0 endif| i in repas]);
%solve satisfy;
solve maximize score_peremptions;

output ["score_peremptions = ", show(score_peremptions), "\n"];
output ["horaire: ", join(" ", [show(horaire[i]) | i in repas])];
