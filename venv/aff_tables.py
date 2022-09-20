import sys
import sqlite3
import magic
import os

# fonctions
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def scan_file(racine):
    liste_db = []
    for dirpath, dirnames, filenames in os.walk(racine):
        for fichier in filenames:
            type_fic = magic.from_file(dirpath+"/"+fichier)
            if type_fic[:19] == "SQLite 3.x database":
                liste_db.append(dirpath+"/"+fichier)
    return liste_db

def list_schemas(db):
    base_lu = sqlite3.connect(db)
    cur = base_lu.cursor()
    cur.execute('select sql from sqlite_master')
    for i in cur.fetchall():
        print(i[0])
    cur.close()

# init vars
racine = ""
i = 1
liste_tables = []
color_rep = colored(194, 1, 20, " ")
color_table = colored(185, 251, 192, " ")
color_select = colored(255, 238, 50, " ")

# recup params
while i < len(sys.argv):
    if i == 1:
        racine = sys.argv[i]
    else:
        liste_tables.append(sys.argv[i])
    i = i + 1

for base in scan_file(racine):
    list_schemas(base)
