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
    dico_table = {}
    cur = base_lu.cursor()
    cur.execute('select sql from sqlite_master')
    for i in cur.fetchall():
        if i[0]:
            if "CREATE TABLE" in i[0]:
                if "IF NOT EXISTS" not in i[0]:
                    decoupe = i[0].split("(")
                    decoupe_table = decoupe[0].split(" ")
                    schema =  decoupe[1]
                    table = decoupe_table[2]
                    dico_table[table] = schema
    cur.close()
    return dico_table

# init vars
racine = ""
i = 1
liste_tables = []
color_rep = colored(194, 1, 20, " ")
color_table = colored(185, 251, 192, " ")
color_select = colored(255, 238, 50, " ")
color_underl = '\033[4m'
color_normal = '\033[0m'
colr_gras = '\033[1m'

# recup params
while i < len(sys.argv):
    if i == 1:
        racine = sys.argv[i]
    else:
        liste_tables.append(sys.argv[i])
    i = i + 1

for base in scan_file(racine):
    dico_schema = list_schemas(base)
    print (colored(0, 255, 255, base)+color_normal)
    for aff_table in dico_schema.keys():
        if aff_table in liste_tables:
            print ("->"+colored(255, 238, 50, aff_table+" "+dico_schema[aff_table])+color_normal)
        else:
            print ("->"+colored(185, 251, 192, aff_table+" "+dico_schema[aff_table])+color_normal)

