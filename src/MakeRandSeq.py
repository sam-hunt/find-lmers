'''
Created on 8/10/2015

@author: Sam Hunt
'''

import random

def random_genome_maker(filename, length):
    with open(filename, 'w') as f:
        f.write(''.join([random.choice(['A ','C ','G ','T ']) for _ in range(length)]))