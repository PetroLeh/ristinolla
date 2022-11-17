### Heat map

Projektin toisella viikolla otin käyttöön taulukon, josta käytän englannin kielistä nimitystä 'heat map'. En oikein keksinyt
sopivaa suomenkielistä nimitystä. Minimax-algoritmin kanssa on ongelmia ja tuntuu turhalta käydä läpi 25 * 25 ruudukon kaikkia
mahdollisia 'siirtoja' kovin pitkälle. Heat mapin tarkoitus on löytää alueet, joihin kannattaa keskittyä.

Ensimmäinen versio heat mapista on sellainen, jossa painottuu ainoastaan pelattujen ruutujen määrä tietyn ruudun ympäristössä.

Toisen version (, jota ei vielä ole) on tarkoitus painottaa ruutuja, joista alkaa kolmen mittaisia suoria tai - jos niihin pelattaisiin - muodostuisi neljän mittaisia suoria.

![kuvakaappaus pelistä](https://github.com/PetroLeh/ristinolla/blob/master/dokumentaatio/kuvat/heat_map.png) 
