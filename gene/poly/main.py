import random

from world import PolynomialWorld, PolynomialOrganism

POOL_SIZE = 6500
TARGET_R2 = 0.10
# Growth Rate = Pb * 2 + Ps # Recommended: Pb = 0.5, Ps = 0.5
BIRTH_PERCENT = 0.50
SURVIVE_PERCENT = 0.5
STARTING_COEFF_BOUNDS = (-100, 100)
STARTING_COEFF_COUNT = (1, 10)

def update_world(world, Pb, Ps):

    world.iteration += 1

    world.mutate_all()

    fitnesses = [(org, org.fitness()) for org in world.organisms]
    fitnesses.sort(key=lambda x:x[1])

    results = []
    for x in xrange(0, int(len(fitnesses) * Pb)):
        cut = fitnesses[x:x + 2]
        if len(cut) > 1:
            patern, matern = cut[0][0], cut[1][0]
            child = matern.spawn(patern)
            results.append(child)

    for index in xrange(0, int(Ps * len(fitnesses))):
        results.append(fitnesses[index][0])

    world.organisms = results

def main():

    world = PolynomialWorld()

    for dummy_count in xrange(POOL_SIZE):
        coeffs = [random.randint(*STARTING_COEFF_BOUNDS) for dummy2 in xrange(random.randint(*STARTING_COEFF_COUNT))]
        world.birth(PolynomialOrganism, *coeffs)

    count = 1
    header = '{count:>5} {population:>6} {r2:>50} {r2max:>50}'.format(count='Count', population='Population', r2='Minimum R2', r2max='Maximum R2')
    print header
    print '-' * len(header)
    while len(world.organisms) > 1:
        fits = [org.fitness() for org in world.organisms]
        r2 = min(fits)
        r2max = max(fits)
        print '{c:>5} {n:>10} {r2:>50f} {r2max:>50f}'.format(c=count, n=len(fits), r2=r2, r2max=r2max)
        #print '%i: Spawning population: pool: %i R2: %f max: %f' % (count, len(world.organisms), r2, r2Max)
        if r2 < TARGET_R2:
            break
        update_world(world, BIRTH_PERCENT, SURVIVE_PERCENT)
        count += 1

    fitnesses = [(org, org.fitness()) for org in world.organisms]
    fitnesses.sort(key=lambda x:x[1])

    chromo, r2 = fitnesses[0]

    print '%s @ R2 = %f' % (chromo, r2)
    print '%s' % world.polynomial



if __name__ == '__main__':
    main()
