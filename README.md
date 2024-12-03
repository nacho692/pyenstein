A simple raycasting engine in python using pygame. 

Python3 is required.

```
pip install -r requirements.txt
python engine.py
```

![Engine sample](readme/sample.png)


TODO (in no particular order):
* Check out floor warping on textures far away
* Speed up floor texturing, rendering loop is pretty slow, and not only because of the blit
* Fix warping on textures on which camera plane intersects, mostly when close to walls
* Add ceiling textures
* Add support for side based textures:
    * Maybe generating a mapping between numbers and customized textures/objects so maps stay simple
    * Raycasting side detection is already implemented
* Add physics for player movement
* Add collision detection
* Implement shaders on textures (super nice to have, don't know how to tackle performance wise)