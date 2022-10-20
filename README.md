A pair of scripts to let me check how accurate it is going from a geotiff raster containing the area of each pixel in WSG84 to h3 cells.

The tl;dr is that at both level 4 and level 8 maginification things seem pretty accurate:

For level 4 (roughly 1770km2 per hex cell):

```
 total: 72731
 under: 717 (0.9858244764955795%)
 within: 71789 (98.70481637816061%)
 over: 225 (0.3093591453438011%)
```

For h3 level 8 (roughly 1km2 per hex cell):

```
 total: 173249851
 under: 113009 (0.0652289161276104%)
 within: 171362366 (98.91054163157693%)
 over: 1774476 (1.0242294522954598%)
```
 
 I ran this with the Jung data map which is 400kx200k pixels WSG84 projection.