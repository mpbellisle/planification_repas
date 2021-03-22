include "CarreMagique.dzn";
include "alldifferent.mzn";

% Constantes
int: n;
int: n_carre = n * n;
int: SOMME_MAGIQUE = n * (n * n + 1) div 2;

% Ensembles
set of int: colonnes = 1..n;
set of int: lignes = 1..n;
set of int: valeurs = 1..n_carre;

% Variables
array[lignes, colonnes] of var valeurs: x;

% Contraintes
constraint all_different([x[i, j] | i in lignes, j in colonnes]) :: bounds;
constraint forall(i in lignes)(sum([x[i, j] | j in colonnes]) = SOMME_MAGIQUE);
constraint forall(j in colonnes)(sum([x[i, j] | i in lignes]) = SOMME_MAGIQUE);
constraint sum([x[i, i] | i in lignes]) = SOMME_MAGIQUE;
constraint sum([x[i, n - i + 1] | i in lignes]) = SOMME_MAGIQUE;

% Bris de symmetries

% On peut prendre un carre magique et permuter les ranges i et n - i + 1
% en meme temps que les colonnes i et n - i + 1 et obtenir un nouveau carre magique
% satisfaisant toutes les contraintes. Par consequent, on peut
% toujours obtenir une solution ou x[i, i] < x[n - i + 1, n - i + 1].
% Si ce n'est pas le cas, on applique la permutation.
constraint forall(i in 1..n div 2)(x[i, i] < x[n - i + 1, n - i + 1]);

% On peut choisir deux entiers 1 <= i < j < n/2. On permutte la rangee i avec j et
% la rangee n - i + 1 avec n - j + 1 de meme que la colonne i avec j et n - i + 1 avec
% n - j + 1. La solution obtenue est un carre magique valide. La consequence est
% qu'on peut faire n'importe quelle permutation sur les floor(n/2) premiers elements
% de la diagonale. On peut donc trier cette partie de la diagonale.
constraint forall(i in 1..n div 2 - 1)(x[i, i] < x[i + 1, i + 1]);

% La transposee d'un carre magique et un carre magique. On peut donc forcer le coin
% superieur droit a etre plus grand (ou plus petit) que le coin inferieur gauche.
constraint x[1, n] > x[n, 1];

solve satisfy;

% Vous pouvez aussi experimenter avec ces variantes de "solve satisfy".
% solve :: int_search(x, first_fail, indomain_min, complete) satisfy;
% solve :: restart_geometric(1.5, 100) satisfy;
%solve :: int_search(x, first_fail, indomain_min, complete) :: restart_geometric(1.5, 100) satisfy;

output ["n = ", show(n), "\n"];
output [join(" ", [show(x[i, j]) | j in colonnes]) ++ "\n" | i in lignes];