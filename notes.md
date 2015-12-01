python, 2d cut cell mesh generator
create a regular mesh in memory
have a function, heightAt(x) that returns z, the surface elevation

walk through all x points, calculate heightAt(x) --> these give us all possible intersections with vertical faces
walk through all z levels, calculate intersectionsAt(z) --> each call gives all intersections with a horizontal surface
add a vertex where terrain intersects horizontal or vertical face of mesh (unless a vertex already exists at that position)
now remove all vertices that lie beneath the ground
add any exposed faces to the ground patch