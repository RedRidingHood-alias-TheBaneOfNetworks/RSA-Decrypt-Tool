# coding: utf-8


################
# interface GUI#
################

from tkinter import *
import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64


GUI = Tk()
GUI.title("RSA Decrypt Tool")
GUI.geometry("1080x700")
GUI.minsize(720, 600)

title = Label(GUI ,text="RSA Decrypt Tool !", font=("Arial",40))
title.pack()

espace1 = Label(GUI, text="")
espace1.pack()

text_modulus = Label(GUI, text="Modulus (decimal) :")
text_modulus.pack()
modulus = Entry(GUI)
modulus.pack()

espace2 = Label(GUI, text="")
espace2.pack()

text_exponent = Label(GUI, text="Exponent (decimal) :")
text_exponent.pack()
exponent = Entry(GUI)
exponent.pack()

text_p = Label(GUI, text="P (decimal factor of the modulus) : ")
text_p.pack()
P = Entry(GUI)
P.pack()

text_p = Label(GUI, text="Q (second decimal factor of the modulus) :")
text_p.pack()
Q = Entry(GUI)
Q.pack()


##################################
# traitement des infos et calcule#
##################################

def traitement():


	n = int(modulus.get())
	e = int(exponent.get())
	q = int(Q.get())
	p = int(P.get())


	phi = (p -1)*(q-1) # affecte à phi la fonction Indicatrice d'Euler (arithmétique)

	def egcd(a, b): # définir la fonction egcd avec a et b en tant que paramètre de la fonction
    		if a == 0: # si le premier argument est égal à 0
        		return (b, 0, 1) # alors afficher le deuxième argument, 0 et 1
    		else: # sinon
        		g, y, x = egcd(b % a, a) # g, y, x = deuxième argument modulo deuxième argument et deuxième argument
        		return (g, x - (b // a) * y, y) # afficher (dans la fonction) g, x moins (b strictement divisé par le premier argument) fois y, y

	def modinv(a, m): # définir la fonction modinv pour calculer l'inverse multiplicatif modulaire avec comme premier argument a et deuxième argument m
    		gcd, x, y = egcd(a, m) # gcd, x et y sont égaux à la focntion egcd avec comme premier argument a et deuxième argument m
    		if gcd != 1: # si gcd n'est pas égal à 1
        		return None # rien afficher
    		else: # sinon
        		return x % m # afficher x modulo m

	d = modinv(e,phi) # affecter à d modinv avec comme premier argument e soit 0x010001 dans l'exemple et comme deuxième argument phi soit (p -1)*(q-1)
	dp = modinv(e,(p-1)) # affecter à dp modinv comme premier argument e, (le nombre premier p - 1)
	dq = modinv(e,(q-1)) # affecter à dq modinv comme premier argument e, (le nombre premier q - 1)
	qi = modinv(q,p) # affecter à qi modinv comme premier argument q et deuxième argument p


	def pempriv(n, e, d, p, q, dP, dQ, qInv): # définir à pempriv les arguments : 1:modulo, 2:exponent, 3 et 4: les deux nombres premiers, 5:e, (le nombre premier q - 1), 6:e, (le nombre premier q - 1), 7:q,p
    		template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n' # affecter à template le début et la fin de la clé
    		seq = pyasn1.type.univ.Sequence() # affecter à seq une séquence pour générer la clé
    		for i,x in enumerate((0, n, e, d, p, q, dP, dQ, qInv)): # pour i et x en énumérant (0 ; modulo ; exponent ; exponent,(p -1)*(q-1) ; les nombres premiers ; (e,(p-1) ; (e,(q-1) ; q,p)
        		seq.setComponentByPosition(i, pyasn1.type.univ.Integer(x)) # encoder en type entier (integer)
    		der = pyasn1.codec.der.encoder.encode(seq) # affecter à der seq mais encodé
    		return template.format(base64.encodestring(der).decode('ascii')) # encoder en ascii der




	key = pempriv(n,e,d,p,q,dp,dq,qi) # affecter à key la fonction pempriv avec tout les paramètres
	decrypted.insert(0, key)

decrypt = Radiobutton(GUI ,text="Crack RSA !",command = traitement)
decrypt.pack()
decrypted = Entry(GUI)
decrypted.pack(padx=10, ipadx=10, ipady=30, pady=30)
text1 = Label(GUI, text="You should use http://factordb.com to find P and Q")
text2 = Label(GUI, text="and use https://www.rapidtables.com/convert/number/hex-to-decimal.html to convert the modulus to an decimal number")
text3 = Label(GUI, text="info : Modulus = P*Q")
text4 = Label(GUI, text="Example : Modulus <=> 00acbe7b776e96f5f357bce84d959ce53ce0029afc0e67901d3602f3275fcc7ec41027b84755e1e64c08ccebae15f9f5efc141892f3882781a35cac58b46797c09 ")
text5 = Label(GUI, text="= 9047341136853946158354084931035401403317236404810122825347899274551597323166322064830737050437362451313263605495279468516338542263888005274643061077015561 (in decimal)")
text1.pack()
text2.pack()
text3.pack()
text4.pack()
text5.pack()


GUI.mainloop()
