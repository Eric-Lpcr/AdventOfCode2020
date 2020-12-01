import time

input_text = """
2004
1867
1923
1819
1940
1675
1992
1728
2006
1578
1630
1893
1910
1509
1569
1967
1917
1922
1919
1813
1870
370
1617
1600
1729
503
1856
1842
1990
1605
1931
1827
1618
1727
1920
1802
1523
1797
1816
1962
1748
1946
1714
1863
1559
1866
1894
1646
1720
1787
1519
1765
562
1823
1639
1697
544
1938
1681
1477
1778
1718
1853
1632
1651
1694
1683
1911
1692
1997
1745
1873
1750
1795
1924
1724
1596
1726
1979
1869
1740
1847
1951
1541
1755
1991
1680
1612
1903
1691
422
1508
1665
1948
1707
1773
1861
1954
2005
1808
1904
543
1678
2001
1688
1855
1258
1695
1877
1554
1568
1771
1857
1597
1738
577
2010
604
1655
1644
1671
1281
1777
1690
1702
1949
1679
1862
1525
1789
1959
1595
1641
1829
1941
1854
1619
1706
1530
1828
1926
1577
1614
1963
1935
1627
1607
1769
111
1647
1716
1696
1868
1021
1906
1575
1905
1668
1758
1915
1892
1663
2003
1943
1742
1883
1576
1510
1546
1734
814
1367
1902
1698
1912
1818
1615
1851
1564
1719
1952
1616
1988
1768
1957
1744
1858
1705
1794
1944
1973
1960
1887
1804
1913
1770
1825
1737
1799
1532
"""


def sum_of_two(data, expected_sum=2020):
    for i, a in enumerate(data):
        b = expected_sum - a
        if b in data[i:]:  # find in remaining numbers only
            return a, b, a * b
    return None


def sum_of_two_v2(data, expected_sum=2020):
    # limitation : this algorithm doesn't ensure that solution is not made of two different numbers...
    # for example, a single 1010 would return a result with it and itself again.
    # solution is not guaranteed to be a strict combination of 2 among 200
    # It would need more code, but the event specification can be interpreted
    data_set = set(data)
    for a in data:
        b = expected_sum - a
        if b in data_set:  # optimized search with set: faster but duplicates data
            return a, b, a * b
    return None


def sum_of_three(data, expected_sum=2020):
    # same distinct element problem here: a and b are guaranted to be different entries,
    # but c may be chosen as a or b
    pair_sum = dict()
    for i, a in enumerate(data):
        for b in data[i:]:  # pair_sum is half a matrix
            s = a + b
            if s <= expected_sum:  # no need for pairs exceeding expected_sum
                pair_sum[a+b] = (a, b)  # keep numbers giving the sum
    for c in data:
        s = expected_sum - c
        if s in pair_sum:  # optimized search with dict
            (a, b) = pair_sum[s]
            return a, b, c, a * b * c
    return None


def main():
    data = [int(n) for n in input_text.split()]

    start_time = time.perf_counter()
    res = sum_of_two_v2(data)
    elapsed_time = time.perf_counter() - start_time
    print("Got", res, "in", elapsed_time, "s")

    start_time = time.perf_counter()
    res = sum_of_three(data)
    elapsed_time = time.perf_counter() - start_time
    print("Got", res, "in", elapsed_time, "s")


if __name__ == '__main__':
    main()
