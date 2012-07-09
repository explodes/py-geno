try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from gene import genes

class PolynomialWorld(genes.World):

    polynomial_coefficients = (1, 1, 2, 3, 5)
    point_range = (0, 25)

    def __init__(self):
        self.iteration = 0
        self.polynomial = PolynomialOrganism(None, *self.polynomial_coefficients)
        self.points = [(x, self.polynomial.evaluate(x)) for x in xrange(*self.point_range)]
        super(PolynomialWorld, self).__init__()

class Polynomial(object):

    def __init__(self, *coefficients):
        self.coefficients = list(coefficients)

    def evaluate(self, x):
        result = 0.
        for index in xrange(len(self.coefficients)):
            result += self.coefficients[index] * (x ** index)
        return result

    def __str__(self):
        io = StringIO()
        num = len(self.coefficients) - 1
        first = True
        cs = self.coefficients[::-1]
        for index, coeff in enumerate(cs):
            if coeff != 0:
                if not first:
                    io.write(' + ')
                else:
                    first = False
                io.write('%fx^%i' % (coeff, num - index))
        return io.getvalue()

class PolynomialOrganism(Polynomial, genes.Organism):

    new_gene_bounds = (-100, 100)
    gene_mutate_variance = (-0.085, 0.085)
    gene_mutate_probability = 0.072
    gene_length_mutate_probability = 0.022

    def __init__(self, world, *coefficients):
        self.dirty = True
        Polynomial.__init__(self, *coefficients)
        genes.Organism.__init__(self, world)

    def fitness(self):
        if self.dirty:
            self._fitness = sum(((self.evaluate(x) - y) ** 2) for x, y in self.world.points) # sum r^2
            self.dirty = False
        return self._fitness

    def spawn(self, patern):
        coeffs = zip(patern.coefficients, self.coefficients)
        genes = []
        for p, m in coeffs:
            avg = (p + m) / 2
            genes.append(avg)
        return PolynomialOrganism(self.world, *genes)

    def mutate(self):
        mutated = False
        for index, gene in enumerate(self.coefficients):
            if self.world.rand() < self.gene_mutate_probability:
                variance = 1 - self.world.rand(*self.gene_mutate_variance)
                gene *= variance
                self.coefficients[index] = gene
                mutated = True
        self.dirty |= mutated
        return mutated

    def clone(self):
        return PolynomialOrganism(self.world, *self.coefficients)

def test():
    world = PolynomialWorld()
    assert len(world.points)
    org = world.birth(PolynomialOrganism, *world.polynomial_coefficients)
    assert org.fitness() == 0

    world.points = [(x, y + 1) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 1 ** 2 * len(xrange(*world.point_range))

    world.points = [(x, y + 1) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 2 ** 2 * len(xrange(*world.point_range))

    world.points = [(x, y + 1) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 3 ** 2 * len(xrange(*world.point_range))

    world.points = [(x, y - 4) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 1 ** 2 * len(xrange(*world.point_range))

    world.points = [(x, y - 1) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 2 ** 2 * len(xrange(*world.point_range))

    world.points = [(x, y - 1) for x, y in world.points]
    org.dirty = True
    assert org.fitness() == 3 ** 2 * len(xrange(*world.point_range))

    print 'TESTS PASSED'

if __name__ == '__main__':
    test()
