
# pelaako tietokone itseään vastaan
AI_VS_AI = False

# ajetaanko testiajo
# testiajot ovat tietokone itseään vastaan ajoja ja niistä kirjoitetaan
# lokitedostot (ei vielä toteutettu)
IS_TEST_RUN = False

# kuinka monta peliä testiajossa pelataan
NUM_OF_TEST_RUNS = 5

# pelialueen sivun pituus
BOARD_SIZE = 20

# voittoon vaadittava suoran pituus
WINNING_LENGTH = 5

# pelaajien (ja tyhjän ruudun) tekstisymbolit
CHARACTERS = {0: ".",
              1: "X",
             -1: "O"
            }

# graafisen käyttöliittymän määrittelyjä:

# näytetäänkö heatmapit
HEAT_MAP = False

# pelaajien värin määrittely graafisessa käyttöliittymässä
player_one_color = (100,100,200)
player_two_color = (200,100,100)

# ruudun koko
CELL_SIZE = 35

# ruutujen välisen seinän paksuus
WALL_THICKNESS = 2
