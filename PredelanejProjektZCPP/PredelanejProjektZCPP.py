
import sqlite3

def nacti_otazky_z_databaze(nazev_databaze):
    otazky = []
    conn = sqlite3.connect(nazev_databaze)
    cursor = conn.cursor()
    cursor.execute("SELECT Otazka, Odpoved1, Odpoved2, Odpoved3, Odpoved4, SpravnaOd FROM Quiz")
    
    for radek in cursor.fetchall():
        text_otazky = radek[0]
        moznosti = [radek[1], radek[2], radek[3], radek[4]]
        spravna_moznost = radek[5]
        otazky.append((text_otazky, moznosti, spravna_moznost))
    
    conn.close()
    return otazky

def spustit_kviz(otazky):
    if not otazky:
        print("Žádné otázky k dispozici.")
        return

    skore = 0
    for text_otazky, moznosti, spravna_moznost in otazky:
        print(text_otazky)
        for i, moznost in enumerate(moznosti, 1):
            print(f"{i}. {moznost}")
        
        odpoved = int(input("Zadejte svou odpověď (1-4): "))
        if odpoved - 1 == spravna_moznost:
            print("Správně!\n")
            skore += 1
        else:
            print(f"Špatně! Správná odpověď byla ({spravna_moznost + 1}. {moznosti[spravna_moznost]})\n")
    
    print(f"Kvíz dokončen!\nZískali jste {skore} z {len(otazky)}.\n")

if __name__ == "__main__":
    nazev_databaze = "Pro3.db"
    otazky = nacti_otazky_z_databaze(nazev_databaze)
    spustit_kviz(otazky)
