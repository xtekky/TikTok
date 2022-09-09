gorgon string -> 04047dcd40000790ed08d0d90bf03d02707a0d90ed0fd06103f0601403507d0b60300c0

```
          0404             7dcd40000                          790ed08d0d90bf03d02707a0d90ed0fd06103f0601403507d0b60300c0

         version    key of string key (there are 31)           encrypted string containing url params, cookies and data
         
       
         1 > base string
                
                a. -> md5 url params (xx=123&xy=123)  + md5 data (us=123)  + md5 cookie = (xx=ededed; dd=eded) + hex timestamp
                b. -> hex list from a.
                
         2 > base string encryption key encrypted with key from list (hex list)
         
         3 > encrypt base string with encryption key
         
         4 > version + hash encryption key key + encrypted hex string
         
 ```  

encrypt key (key is hex list)

```py
    Z = 256
    Y = encryption hex list from defined list (31 possibilities)
    
    def __encryption_key(self, Z: int, HX: list):
        tmp = A = B = C = D = None
        hexs = []

        for i in range(Z):
            hexs.append(i)

        for i in range(Z):
            if i == 0:
                A = 0
            elif tmp is not None:
                A = tmp
            else:
                A = hexs[i - 1]
            B = HX[i % 8]
            if (A == 85) & (i != 1) & (tmp != 85):
                A = 0
            C = self.__hex_max(A + i + B)
            tmp = C if C < i else None
            D = hexs[C]
            hexs[i] = D
        return hexs
```

encrypt with key
```py


    def __xor_hash_list(self, HL, HK):
        tmp_add = []
        tmp_hex = [] + HK
        A = B = C = D = E = F = G = None
        rang = self.__calc_ranges(self.LEN)
        for i in rang:
            A = HL[i]
            B = 0 if len(tmp_add) == 0 else tmp_add[-1]
            C = self.__hex_max(HK[i + 1] + int(B))
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = self.__hex_max(D + D)
            F = tmp_hex[E]
            G = A ^ F
            HL[i] = G

        return HL

```
