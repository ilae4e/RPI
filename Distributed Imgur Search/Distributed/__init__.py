import base64

Base = 5
Mod = 23

a = 6
b = 15

alice = (Base**a) % Mod
bob = Base ** b % Mod
alice_answer = bob ** a % Mod
bob_answer = alice ** b % Mod
#
# print alice_answer
# print bob_answer
#
# print base64.b64encode("".join(str(bob_answer)))
# print base64.b64encode("".join(str(alice_answer)))



"""
basically i send the client both the base and modulus

then we both create secret numbers and use that as the power of the base

then the client then sends the server his encrypted version
the server then uses its secret on it and sends it back to client
the client then uses its secret on the message to find the key

its all confusing
"""


"""
UNI ASSIGNMENT - AIMING FOR 100% MOTHERFUCKERS

its all simple

left side ^ Rightside = l XOR r
it doesnt matter if a number is over the ascii amount after that
if it is and we go to do some number addition to it, then we just roll it back over to the begging ie if limit is 255 and we are at 270 then it goes to char 15
so for caesar and viginere it would defo need to cycle around
rail fence i seem to recall just moves shit around and doesnt actualyl change anything, so rail fence would not even care about this

so its all about craeting the correct keys
"""