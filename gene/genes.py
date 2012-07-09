

class prettyobject(object):

    def __str__(self):
        return self.__class__.__name__

class World(prettyobject):
    ''' Describes the state of the world organisms live in '''

    def __init__(self):
        import random
        self._random = random
        self.organisms = []

    def birth(self, OrganismKlass, *args, **kwargs):
        born = OrganismKlass(self, *args, **kwargs)
        self.organisms.append(born)
        return born

    def spawn(self, matern, patern):
        born = patern.spawn(matern)
        self.organisms.append(born)
        return born

    def kill(self, organism):
        self.organisms.remove(organism)

    def clone(self, organism):
        born = organism.clone()
        self.organisms.append(born)
        return born

    def mutate_all(self):
        for organism in self.organisms:
            organism.mutate()

    def rand(self, min_val=0, max_val=1):
        return min_val + (max_val - min_val) * self._random.random()

class Organism(prettyobject):

    def __init__(self, world):
        self.world = world

    def fitness(self):
        return 0

    def spawn(self, patern):
        return self.clone()

    def mutate(self):
        return False

    def clone(self):
        return self.__class__(self.world)

def test():
    assert str(prettyobject()) == 'prettyobject'
    world = World()
    assert len(world.organisms) == 0
    organism = world.birth(Organism)
    assert len(world.organisms) == 1
    assert world.organisms[0] == organism
    assert organism.clone().world == world
    assert organism.fitness() == 0
    assert organism.mutate() == False
    assert isinstance(world.spawn(organism, organism.clone()), Organism)
    assert len(world.organisms) == 2
    assert isinstance(world.clone(organism), Organism)
    assert len(world.organisms) == 3
    world.kill(organism)
    assert len(world.organisms) == 2

    print 'TESTS PASSED'


if __name__ == '__main__':
    test()






