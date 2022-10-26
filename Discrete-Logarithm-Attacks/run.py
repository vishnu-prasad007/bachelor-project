from brute_force import brute
from bsgs import bsgs
from pohlig_hellman import pohlig_hellman
from pollard_rho import pollard_rho


print('1. Baby-Step, Gaint-Step Algorithm')
print('2. Pollard-rho Algorithm')
print('3. Pohling-Hellman Algorithm')
print('Choose your attack')
selected_attack = int(input())
print('Enter the Generator for P : ')
g = int(input())
print('Enter the prime value : ')
n = int(input())
print('Enter the shared secret: ')
y = int(input())
    
if selected_attack == 1:
    x = bsgs(g,y,n)
elif selected_attack == 2:
    x = pollard_rho(g,y,n)
elif selected_attack == 3:
    prime_factors = list(map(int,input("\nEnter Prime factors of n-1 :  ").strip().split()))[:n]
    x = pohlig_hellman(g,y,n,factors=prime_factors,powers=[1,1])

print('X->>>',x)