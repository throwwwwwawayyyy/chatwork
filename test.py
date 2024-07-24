class B:
    @staticmethod
    def test():
        print("test")

b = B()
t = type(b)
t.test()