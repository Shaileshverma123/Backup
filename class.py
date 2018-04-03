class ComplexNumber:
   real = 0
   img = 0
   def __init__(self,r,i):
       print("constructor called")
       self.real = r
       self.img = i

   def add(self,c):
       self.real = self.real + c.real
       self.img = self.img + c.img

   def printer(self):
       print(str(self.real) + "," + str(self.img))


ComplexObject = ComplexNumber(15,53)
print("This is the value of object 1")
ComplexObject.printer()
Complex2 = ComplexNumber(2,1)
print("This is the value of object 2")
Complex2.printer()
ComplexObject.add(Complex2)
ComplexObject.printer()