import csv
from datetime import datetime
from prettytable import PrettyTable

# =========================
# LECTURE CSV
# =========================
L = []

with open("donnee.csv", "r", encoding="latin-1") as f:
    lecture = csv.DictReader(f, delimiter=";")
    for ligne in lecture:
        L.append(ligne)

# =========================
# VALIDATION CLASSE
# =========================
def verifier_classe(classe):
    erreurs = []

    if not classe or classe.strip() == "":
        return ["Classe vide"], None

    classe = classe.replace(" ", "").lower()

    if len(classe) < 2:
        return ["Classe invalide"], None

    niveau = classe[0]
    section = classe[-1]

    if niveau not in ["3", "4", "5", "6"]:
        erreurs.append("Niveau invalide")

    if section not in ["a", "b", "c", "d"]:
        erreurs.append("Section invalide")

    if erreurs:
        return erreurs, None

    return [], niveau + "eme " + section.upper()


# =========================
# VALIDATION DATE
# =========================
def verifier_date(date_str):
    if not date_str or date_str.strip() == "":
        return ["Date vide"], None

    date_str = date_str.replace("-", "/").replace(".", "/")

    formats = ("%d/%m/%Y", "%d/%m/%y")

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return [], dt.strftime("%d/%m/%Y")
        except:
            pass

    return ["Format date invalide"], None


# =========================
# VALIDATION NOTES
# =========================
def verifier_notes(notes_str):
    if not notes_str or notes_str.strip() == "":
        return ["Notes vides"], None

    try:
        matieres = notes_str.split("#")
        resultats = []

        for m in matieres:
            nom = m.split("[")[0]
            contenu = m.split("[")[1].replace("]", "")

            devoirs_str, examen_str = contenu.split(":")

            devoirs = [float(x.replace(",", ".")) for x in devoirs_str.split("|")]
            examen = float(examen_str.replace(",", "."))

            moyenne = (sum(devoirs) / len(devoirs) + 2 * examen) / 3

            resultats.append({
                "matiere": nom,
                "moyenne": round(moyenne, 2)
            })

        return [], resultats

    except:
        return ["Erreur notes"], None


# =========================
# SEPARATION VALIDE / INVALIDE
# =========================
def separer_valide_invalide(L):
    valides = []
    invalides = []

    for ligne in L:
        erreurs = []

        err_c, classe = verifier_classe(ligne.get("Classe", ""))
        err_d, date = verifier_date(ligne.get("Date de naissance", ""))
        err_n, notes = verifier_notes(ligne.get("Note", ""))

        erreurs += err_c + err_d + err_n

        if erreurs:
            ligne["Erreurs"] = " ; ".join(erreurs)
            invalides.append(ligne)
        else:
            ligne["Classe"] = classe
            ligne["Date de naissance"] = date
            ligne["Notes"] = notes
            valides.append(ligne)

    return valides, invalides


# =========================
# EXECUTION
# =========================
valides, invalides = separer_valide_invalide(L)

print("\n===== RESULTATS =====")
print("Nombre d'élèves valides   :", len(valides))
print("Nombre d'élèves invalides :", len(invalides))


# =========================
# AFFICHAGE (OPTIONNEL)
# =========================
def afficher(tableau, titre):
    table = PrettyTable()
    table.title = titre

    if len(tableau) == 0:
        print("Aucune donnée")
        return

    colonnes = tableau[0].keys()
    table.field_names = colonnes

    for row in tableau:
        table.add_row([row.get(col, "") for col in colonnes])

    print(table)


# =========================
# MENU SIMPLE
# =========================
def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Voir valides")
        print("2 - Voir invalides")
        print("3 - Statistiques")
        print("4 - Quitter")

        choix = input("Choix : ")

        if choix == "1":
            afficher(valides, "ÉLÈVES VALIDES")

        elif choix == "2":
            afficher(invalides, "ÉLÈVES INVALIDES")

        elif choix == "3":
            print("Valides :", len(valides))
            print("Invalides :", len(invalides))

        elif choix == "4":
            break


menu()