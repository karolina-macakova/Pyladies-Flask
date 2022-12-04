# Pyladies-Flask

 TODO list - zadání
Vytvořte flask server, který bude implementovat TODO list. Na serveru bude TODO list uložen v textovém souboru (jeden řádek = jedna položka TODO seznamu).

1. krok

Každá položka TODO listu bude zatím jen řetězec (písmena bez háčků a čárek, číslice, podtržítko) a ten bude sloužit současně jako identifikátor. Možné názvy úkolů tedy jsou například: Ukol1, Dokonci_stage1

● podporované requesty:
1. GET /todos - vrátí seznam všech TODO
2. POST /todo
body: jmeno_polozky
přidá novou položku
3. DELETE /todo/Ukol1 - smaže Ukol1

● Jakékoliv chybné requesty by měly bý ošetřeny (např. neexistující TODO nebo nevalidní vstup u POST /todo).


2. krok

V prvním kroku jsme pouze načrtli řešení. Nyní se ho pokusíme předělat to uživatelsky přívětivější podoby. Hlavními problémy jsou nemožnost zvolit si libovolný text jako TODO položku a nemožnost si odškrtávat úkoly jako hotové. TODO položku tedy rozšíříme. Nyní bude obsahovat několik nových informací, tj.:
1. identifikátor (zůstane z kroku 1)
2. text
3. status (is_done; True nebo False podle toho, zda je úkol hotový)

Nové a změněné requesty:
● POST /todo; body: jmeno,popisek - přidá novou položku se statusem is_done=False
● PUT /Ukol1/set-done - označí úkol jako hotový
● PUT /Ukol1/set-not-done - označí úkol jako nový


3. krok

Přidáme deadline a možnosti filtrování TODO položek. Každá položka nyní tedy bude obsahovat toto:
● identifikátor (zůstane z kroku 2)
● text (zůstane z kroku 2)
● status (zůstane z kroku 2)
● deadline

Cílem bude rozšířit GET /todos tak, abychom mohli získat i následující informace:
● GET /todos?date_from=2022-01-01&date_to=2022-01-02 - všechny TODO položky v nějakém časovém intervalu
● GET /todos?date_from=now&count=1&sort_by=urgency - jedna položka s nejvíc hořícím deadlinem
● GET /most-urgent - totéž
● GET /todos?date_to=now&is_done=False - všechny položky, které nejsou hotové, přestože už jsou po deadlinu

Dále samozřejmě musíme aktualizovat přidávání položky o deadline:
● POST /todo
body: Ukol1, 2022-11-22, Text úkolu 1 - přidá novou položku se statusem is_done=False
