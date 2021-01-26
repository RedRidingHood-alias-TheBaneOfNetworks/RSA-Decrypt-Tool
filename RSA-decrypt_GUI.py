# coding: utf-8

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


def traitement():


	n = int(modulus.get())
	e = int(exponent.get())
	q = int(Q.get())
	p = int(P.get())


	phi = (p -1)*(q-1)

	def egcd(a, b):
    		if a == 0:
        		return (b, 0, 1)
    		else:
        		g, y, x = egcd(b % a, a)
        		return (g, x - (b // a) * y, y)
		
	def modinv(a, m):
    		gcd, x, y = egcd(a, m)
    		if gcd != 1:
        		return None
    		else:
        		return x % m

	d = modinv(e,phi)
	dp = modinv(e,(p-1))
	dq = modinv(e,(q-1))
	qi = modinv(q,p)


	def pempriv(n, e, d, p, q, dP, dQ, qInv):
    		template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    		seq = pyasn1.type.univ.Sequence()
    		for i,x in enumerate((0, n, e, d, p, q, dP, dQ, qInv)):
        		seq.setComponentByPosition(i, pyasn1.type.univ.Integer(x))
    		der = pyasn1.codec.der.encoder.encode(seq)
    		return template.format(base64.encodestring(der).decode('ascii'))



	key = pempriv(n,e,d,p,q,dp,dq,qi)
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
