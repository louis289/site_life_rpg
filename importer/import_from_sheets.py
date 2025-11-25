import os
import time
import io
import csv
import requests
import mysql.connector


def wait_for_db(config, timeout=60):
    """Attend que MySQL soit prêt."""
    start = time.time()
    while True:
        try:
            conn = mysql.connector.connect(**config)
            conn.close()
            print("MySQL est prêt.")
            return
        except mysql.connector.Error as e:
            if time.time() - start > timeout:
                raise RuntimeError("Temps dépassé en attendant MySQL") from e
            print("En attente de MySQL...", e)
            time.sleep(2)


def get_db_config():
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", "3306")),
        "user": os.environ.get("DB_USER", "life"),
        "password": os.environ.get("DB_PASSWORD", "life"),
        "database": os.environ.get("DB_NAME", "life_rpg"),
    }


def fetch_csv(url: str) -> csv.DictReader:
    print(f"Téléchargement du CSV depuis : {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    # Le CSV est renvoyé en texte
    content = resp.content.decode("utf-8")
    csv_file = io.StringIO(content)
    reader = csv.DictReader(csv_file)

    print("Colonnes détectées dans le CSV :", reader.fieldnames)
    return reader


def import_quests(cursor, reader):
    """
    Mappe les colonnes du sheet vers la table quests.
    On suppose les en-têtes :
      Nom de l'Arc, Arc, Fréquence, Quete, XP / Quête, Intensité,
      Répétition, Statut, Type, Barème
    """

    insert_sql = """
        INSERT INTO quests (
            nom_arc, arc, frequence, quete,
            xp_par_quete, intensite, repetition,
            statut, type_quete, bareme
        )
        VALUES (
            %(nom_arc)s, %(arc)s, %(frequence)s, %(quete)s,
            %(xp_par_quete)s, %(intensite)s, %(repetition)s,
            %(statut)s, %(type_quete)s, %(bareme)s
        )
    """

    count = 0
    for row in reader:
        # Parsing / nettoyage de base
        def to_int(value):
            value = value.strip() if isinstance(value, str) else value
            if not value:
                return None
            try:
                return int(float(value.replace(',', '.')))
            except ValueError:
                return None

        data = {
            "nom_arc": row.get("Nom de l'Arc", "").strip(),
            "arc": row.get("Arc", "").strip(),
            "frequence": row.get("Fréquence", "").strip(),
            "quete": row.get("Quete", "").strip(),
            "xp_par_quete": to_int(row.get("XP / Quête", "")),
            "intensite": to_int(row.get("Intensité", "")),
            "repetition": to_int(row.get("Répétition", "")),
            "statut": row.get("Statut", "").strip(),
            "type_quete": row.get("Type", "").strip(),
            "bareme": row.get("Barème", "").strip(),
        }

        cursor.execute(insert_sql, data)
        count += 1

    print(f"{count} quêtes insérées dans la base.")


def main():
    db_config = get_db_config()
    sheet_url = os.environ.get("SHEET_URL_QUESTS")

    if not sheet_url:
        raise RuntimeError("La variable d'environnement SHEET_URL_QUESTS n'est pas définie.")

    # 1. Attendre que MySQL soit prêt
    wait_for_db(db_config)

    # 2. Récupérer le CSV du Google Sheet
    reader = fetch_csv(sheet_url)

    # 3. Insérer dans MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        import_quests(cursor, reader)
        conn.commit()
        print("Import terminé avec succès.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
