### viikkoraportti
#### viikko 6

Projekti oli jonkin aikaa paitsiossa muiden töiden takia. Puolittain toimivan algoritmin ongelmana oli se, että se
lähinnä rakenteli tilanteita, mutta ei sitten tehnyt voittaavaa suoraa selvästä tilanteesta. Lisäksi se oli erittäin hidas.

Korjasin tuota 'jatkuvaa rakentelua' -ongelmaa ja tehostin algoritmia. En ole vain aivan varma teinkö sen "oikein" mitä tulee kurssin vaatimuksiin.
En juurikaan koskenut itse minimax-algoritmiin, vähän siihenkin, mutta enimmäkseen tehostus tapahtui karsimalla ja tarkastamalla siirtovaihtoehtoja
jo ennen minimax-laskentaa.

Lisäsin mahdollisuuden tekoälyn pelata itseään vastaan. Jossain vaiheessa työn alla oli kaksi versiota minimaxista, jotka olisivat voineet pelata
toisiaan vastaan ja näistä peleistä oli tarkoitus koota testiaineisto, jolla verrata eri versioita. Algoritmeissa oli vain pieniä eroja mm. pelitilanteen
arvioinnissa ja toisessa oli hajautustaulu jo arvioituja tilanteita varten. Toinen algoritmi oli kuitenkin huomattavasti hitaampi eikä useissa testipeleissä
näyttänyt olevan toiminnan kannalta eroja. Jätin kuitenkin lopulta vain tehokkaamman, sen joka karsii vaihtoehtoja raaemmin.

Lisäilin koodiin kommentteja ja lisäsin testejä

pylint-siivous on vielä tekemättä

Jonkin näköinen testiajokirjasto/moduuli olisi vielä tarkoitus tehdä, jos aikaa riittää.
