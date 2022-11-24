# Ristinolla
### tietorakenteet ja algoritmit -harjoitustyö
### syksy 2022

[Määrittelydokumentti](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/maarittelydokumentti.md)

#### raportit
- [viikkoraportti 1](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/viikkoraportti_1.md)
- [viikkoraportti 2](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/viikkoraportti_2.md)
- [viikkoraportti 3 (myöhässä)](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/viikkoraportti_3.md)

---

#### asennus
- kopioi repositorion sisältö koneellesi
- asenna riippuvuudet komennolla `poetry install` projektin juurihakemistossa

##### käynnistys
- käynnistä ohjelma komennolla `python3 ristinolla.py` tai `poetry run python3 ristinolla.py`

- käynnistäessä voi antaa kännistysargumentteja:
    - `-t` tai `--text`: ohjelma käynnistyy tekstikäyttöliittymässä
    - `-hm` tai `--heat_map`: graafisessa käyttöliittymässä tulee näkyviin pari versiota ["heat mapeista"](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/heat_map.md)
    - `<N>:<M>`: pelialue on N*N ruudukko ja M on voittoon tarvittava pituus (N=3-25 M=3-6)

##### testit
testit saa ajettua komennolla `poetry run pytest`

---

#### muuta
- Kuulen mielelläni, jos jokin asia ei toimi...
