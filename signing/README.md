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
