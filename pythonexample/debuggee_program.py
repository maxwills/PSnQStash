class MyClass:
        
    def methodA(self):
        w = 1
        return w

    def methodB(self):
        x = 2
        self.methodC()
        return x

    def methodC(self):
        y = 3
        return y

    def methodD(self):
        z = 4
        return z

def main():
    obj = MyClass()
    obj.methodA()
    obj.methodB()
    obj.methodD()

main()