
# pelaako tietokone itseään vastaan
ai_vs_ai = False

# ajetaanko testiajo
# testiajot ovat tietokone itseään vastaan ajoja ja niistä kirjoitetaan lokitedostot (ei vielä toteutettu)
is_test_run = False

# kuinka monta peliä testiajossa pelataan
num_of_test_runs = 5

# pelialueen sivun pituus
board_size = 20

# voittoon vaadittava suoran pituus
winning_length = 5

# maksimi syvyys minimax-algoritmissa
max_depth_in_minimax = 6

# pelaajien (ja tyhjän ruudun) tekstisymbolit
characters = {0: ".",
              1: "X",
             -1: "O"
            }

# graafisen käyttöliittymän määrittelyjä:

# näytetäänkö heatmapit
heat_map = False

# pelaajien värin määrittely graafisessa käyttöliittymässä
player_one_color = (100,100,200)
player_two_color = (200,100,100)

# ruudun koko
cell_size = 35

# ruutujen välisen seinän paksuus
wall_thickness = 2
