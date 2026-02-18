#!/usr/bin/env python3
from sys import argv
from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre


def decoupe(facettes, epaisseur):
    """
    renvoie un vecteur de vecteurs de segments.
    chaque vecteur interne contient tous les segments 2d d'une seule tranche.
    le vecteur externe contient toutes les coupes de tranches de la plus basse (x minimal)
    a la plus haute (x maximal).
    """
    if not facettes:
        return []
    z_min = min(f.zmin_et_zmax()[0] for f in facettes)
    z_max = max(f.zmin_et_zmax()[1] for f in facettes)
    hauteurs = multiples_entre(z_min, z_max, epaisseur)
    print("z_min:", z_min, "z_max:", z_max)
    print("hauteurs:", hauteurs)
    tranches = []
    for h in hauteurs:
        segments_tranche = []
        #for f in facettes:
            #seg = f.intersection_plan_horizontal(h)
            #if seg:
                #segments_tranche.append(seg[0])
        #tranches.append(segments_tranche)

        #On peut filtrer les facettes hors tranche pour éviter de calculer des intersections inutiles
        for f in facettes:
            zmin_f, zmax_f = f.zmin_et_zmax()
            if h < zmin_f or h > zmax_f:
                continue  # pas d'intersection possible
            segments_tranche.extend(f.intersection_plan_horizontal(h))
        tranches.append(list(segments_tranche))

    return tranches
        
        


def main():
    if len(argv) != 3:
        print("donnez un nom de fichier stl, une epaisseur de tranches")
        exit()
    fichier_stl = argv[1]
    epaisseur = float(argv[2])

    facettes = list(
        f for f in facettes_stl_binaire(fichier_stl) if not f.est_horizontale()
    )
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)

    for tranche in tranches:
        affiche(tranche)


if __name__ == "__main__":
    main()
