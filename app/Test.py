import unittest
import testingcode

n1 = int(input("Enter First Number :"))
n2 = int(input("Enter Second Number :"))
rsadd = int(input("Enter Expect Number of Add:"))
rsubtract = int(input("Enter Expect Number of Sub :"))
rsmulti = int(input("Enter Expect Number of Multi :"))
rsdivid = float(input("Enter Expect Number of Divide :"))
rhcf = float(input("Enter Expect HCF of given number :"))


class TestCal(unittest.TestCase):
    def test_add(self):
        rsa = testingcode.add(n1, n2)
        self.assertEqual(rsa, rsadd)

    def test_sub(self):
        rss = testingcode.subst(n1, n2)
        self.assertEqual(rss, rsubtract)

    def test_multi(self):
        rsm = testingcode.multi(n1, n2)
        self.assertEqual(rsm, rsmulti)

    def test_divide(self):
        rsd = testingcode.div(n1, n2)
        self.assertEqual(rsd, rsdivid)

    def test_hcf(self):
        rshcf = testingcode.comput_hcf(n1, n2)
        self.assertEqual(rshcf, rhcf)
