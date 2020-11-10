import sys, os
import multiprocessing as mp
import numpy as np
from itertools import count, takewhile, islice, accumulate, chain, cycle

manager = mp.Manager()
caixa = manager.dict()

def sieve8(n):
    """Return an array of the primes below n."""
    prime = np.ones(n//3 + (n%6==2), dtype=np.bool)
    for i in range(3, int(n**.5) + 1, 3):
        if prime[i // 3]:
            p = (i + 1) | 1
            prime[       p*p//3     ::2*p] = False
            prime[p*(p-2*(i&1)+4)//3::2*p] = False
    result = (3 * prime.nonzero()[0] + 1) | 1
    result[0] = 3
    return np.r_[2,result]


def wsieve():       # ideone.com/mqO25A
    wh11 = [ 2,4,2,4,6,2,6,4,2,4,6,6, 2,6,4,2,6,4,6,8,4,2,4,2,
             4,8,6,4,6,2,4,6,2,6,6,4, 2,4,6,2,6,4,2,4,2,10,2,10]
    cs = accumulate( chain( [11], cycle( wh11)))
    yield( next( cs))  # cf. ideone.com/WFv4f
    ps = wsieve()      #     codereview.stackexchange.com/q/92365/9064
    p = next(ps)       # 11         stackoverflow.com/q/30553925/849891
    psq = p*p          # 121
    D = dict( zip( accumulate( chain( [0], wh11)), count(0)))   # start from
    mults = {}
    for c in cs:
        if c in mults:
            wheel = mults.pop(c)
        elif c < psq:
            yield c ; continue
        else:          # c==psq:  map (p*) (roll wh from p) = roll (wh*p) from (p*p)
            x = [p*d for d in wh11]
            i = D[ (p-11) % 210]
            wheel = accumulate( chain( [psq+x[i]], cycle( x[i+1:] + x[:i+1])))
            p = next(ps) ; psq = p*p
        for m in wheel:
            if not m in mults:
                break
        mults[m] = wheel


def primes_():
	yield from (2, 3, 5, 7)
	yield from wsieve()


def follow_path(dirty_number, append):
    append(caixa[dirty_number][1])
    new_dirty_number = caixa[dirty_number][0]

    if new_dirty_number in caixa:
        new_dirty_number = follow_path(new_dirty_number, append)

    return new_dirty_number

def factorize_numbers(numbers):
    answer = dict()
    step = 10000
    for number in numbers:
        start = 0
        sieve = list(islice(primes_(), start, start + step))
        answer_number = []
        append = answer_number.append
        dirty_number = number
        broke = False
        while True:
            for p in sieve: 
                while dirty_number % p == 0: 
                    if dirty_number in caixa:
                        dirty_number = follow_path(dirty_number, append)
                    else:
                        caixa[dirty_number] = (dirty_number // p, p)
                        append(p)
                        dirty_number //= p

                if p*p > number:
                    broke = True
                    break
            
            if broke:
                if p < dirty_number:
                    caixa[dirty_number] = (1, dirty_number)
                    append(dirty_number)

                break
            
            start += step
            sieve = list(islice( primes_(), start, start + step))

        answer[number] = answer_number

    return answer


class OtherClass:
    def factorize_number(self, number):
        start = 0
        step = 10000
        sieve = list(islice(primes_(), start, start + step))
        answer_number = []
        append = answer_number.append
        dirty_number = number
        broke = False
        while True:
            for p in sieve: 
                while dirty_number % p == 0: 
                    if dirty_number in caixa:
                        dirty_number = follow_path(dirty_number, append)
                    else:
                        caixa[dirty_number] = (dirty_number // p, p)
                        append(p)
                        dirty_number //= p

                if p*p > number:
                    broke = True
                    break
            
            if broke:
                if p < dirty_number:
                    caixa[dirty_number] = (1, dirty_number)
                    append(dirty_number)

                break
            
            start += step
            sieve = list (islice(primes_(), start, start + step))

        return answer_number

    def follow_path(self, dirty_number, append):
        append(caixa[dirty_number][1])
        new_dirty_number = caixa[dirty_number][0]

        if new_dirty_number in caixa:
            new_dirty_number = self.follow_path(new_dirty_number, append)

        return new_dirty_number


class SomeClass:
    def some_method(self, numbers):
        with mp.Pool(mp.cpu_count() - 1) as pool:
            other = OtherClass()
            return list(pool.map(other.factorize_number, numbers))


def factorize(numbers):
    """
        A Faire:         
        - Ecrire une fonction qui prend en paramètre une liste de nombres et qui retourne leurs decompositions en facteurs premiers
        - cette fonction doit retourner un dictionnaire Python où :
            -- la clé est un nombre n parmi la liste de nombres en entrée
            -- la valeur est la liste des facteurs premiers de n (clé). Leur produit correpond à n (clé).  
            
        - Attention : 
            -- 1 n'est pas un nombre premier
            -- un facteur premier doit être répété autant de fois que nécessaire. Chaque nombre est égale au produit de ses facteurs premiers. 
            -- une solution partielle est rejetée lors de la soumission. Tous les nombres en entrée doivent être traités. 
            -- Ne changez pas le nom de cette fonction, vous pouvez ajouter d'autres fonctions appelées depuis celle-ci.
            -- Ne laissez pas trainer du code hors fonctions car ce module sera importé et du coup un tel code sera exécuté et cela vous pénalisera en temps.
    """
    
    if max(numbers) < 10e10:
        return factorize_numbers(numbers)

    results = SomeClass().some_method(numbers)

    answer = dict()
    for i in range(len(numbers)):
        answer[numbers[i]] = results[i]

    return answer # ceci n'est pas une bonne réponse

#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des fichiers en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # un repertoire pour enregistrer les résultats doit être passé en parametre 2
    if not os.path.isdir(output_dir):
	    print(input_dir, "doesn't exist")
	    exit()       

     # Pour chacun des fichiers en entrée 
    for data_filename in sorted(os.listdir(input_dir)):
        # importer la liste des nombres
        data_file = open(os.path.join(input_dir, data_filename), "r")
        numbers = [int(line) for line in data_file.readlines()]        
        
        # decomposition en facteurs premiers
        D = factorize(numbers)

        # fichier des reponses depose dans le output_dir
        output_filename = 'answer_{}'.format(data_filename)             
        output_file = open(os.path.join(output_dir, output_filename), 'w')
        
        # ecriture des resultats
        for (n, primes) in D.items():
            output_file.write('{} {}\n'.format(n, primes))
        
        output_file.close()

    
