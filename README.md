## Sync: Virtual, Synchronizing Fireflies

A synchronization experiment inspired by the book "Sync: How Order Emerges
From Chaos In the Universe, Nature, and Daily Life" by Steven H. Strogatz.

Each cell flashes roughly once every few seconds. The cells
influence each other in such a way that they all eventually synchronize,
similar to synchronizing fireflies.

There is a 2-D implementation (wxPython) and a 3-D implementation (Pyglet).

Several configuration parameters are available...

* Grid Width, Height and Depth
* Simulation Speed
* Average Cell Period
* Influence Factor
* Cell Similarity Factor

Each cell charges following a curve similar to a charging capacitor. When
the cell reaches a threshold, it fires causing a blink in the visualization.
The cell firing also kicks neighboring cells by a factor proportional to the
inverse of their squared distance. The cells need not have identical 
individual frequencies to reach sychronization. This can be tested by tweaking
the similarity factor, which causes the cells to vary in their charging times.

## Video

http://www.youtube.com/watch?v=1G6GHQ-EbJI

## Screenshot (2-D)

![Screenshot](https://raw.github.com/fogleman/Sync/master/screenshot-2d.png)

## Screenshot (3-D)

![Screenshot](https://raw.github.com/fogleman/Sync/master/screenshot-3d.png)
