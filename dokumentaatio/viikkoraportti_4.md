### viikkoraportti
#### viikko 4

Sain minimaxin toimimaan. Ongelma ratkesi siirtämällä voiton tarkistus eri kohtaan.

vanha (versio 1):

```

def minmax(args):

  if voitto:
    return 1 if max else -1
    
  if jokuMuuSyyLopettaaLaskenta:
    return 0
   
  if max:
    for move in moves:
      score = minmax(args)
      # ...
   
  if min:
    for move in moves:
      score = minmax(args)
      # ...
      
```

uusi (versio 2):

```

def minmax(args):

  if jokuMuuSyyLopettaaLaskenta:
    return 0
  
  if max:
    for move in moves:
      if voitto:
        return 1
      score = minmax(args)
      # ...
   
  if min:
    for move in moves:
      if voitto:
        return -1
      score = minmax(args)
      # ...
      
```

Ongelmana taisi olla se, että voitontarkistuksen olen toteuttanut niin, että se tapahtuu funktiossa `Board.is_winning(move, player)`
jossa ei tarkisteta koko pelialuetta, vaan vain muodostaako argumenttina saatu siirto voittavan suoran. Funktio saa argumenttina myös
pelaajan, jonka siirto on kyseessä. Versiossa 1 vuoro maksimoijan ja minimoijan välillä on jo vaihtunut, mutta tehty siirto on vielä
edellisen vuoron jäljiltä. Mielestäni otin tämän huomioon voitontarkistuksessa, mutta ilmeisesti väärin, koska ongelma ratkesi tuolla
tarkistuksen siirrolla.

Kaikenlaisten himmeleiden jäljiltä koodissa on siivottavaa. Seuraavaksi siis kaikkea sitä mikä nyt on jäänyt tekemättä siis siivoamista, kommentointia, testausta ja algoritmin tehostamista.



