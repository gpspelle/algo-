import sys, os
import numpy as np

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


sieve = sieve8(10000)

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

    global sieve
    answer = dict()

    for number in numbers:
        answer[number] = []
        dirty_number = number
        p = 2
        while not(dirty_number % p > 0):
            dirty_number >>= 1;
            answer[number].append(p)

        for p in sieve: 
            while dirty_number % p == 0: 
                answer[number].append(p)
                dirty_number = dirty_number // p

            if p*p > dirty_number:
                break

        if p < dirty_number:
            answer[number].append(dirty_number)

        p = sieve[-1]
        while p*p <= dirty_number:
            if dirty_number % p == 0:
                answer[number].append(p)
                dirty_number = dirty_number // p
            else:
                p += 2

        if p < dirty_number:
            answer[number].append(dirty_number)
                
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

    
