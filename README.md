#Visualize the bacteriome using NetworkX
A python script that uses [NetworkX] (https://networkx.github.io/) to make a .png figure of [the bacteriome interaction network] (http://www.compsysbio.org/bacteriome/).

###Sample output file
![output file](/output.png)

###Example

'''
$ python network_generator.py
network has 2275 nodes with 7553 edges
Enter the confidence threshold cutoff (0 - 1.0). 0.9
network filtered by confidence 0.90 has 619 nodes with 1844 edges
Enter the minimum degree for each node displayed in network. 30
network filtered by nodes with more than 30 connections has 250 nodes with 689 edges
'''