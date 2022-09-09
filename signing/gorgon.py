import time
import random
import hashlib


class Gorgon:
    def __init__(self, params: str) -> None:
        self.params   = params
        self.DGTS     = {c: i for i, c in enumerate("0123456789abcdefghijklmnopqrstuvwxyz")}
        self.HASHES   = ['c8dc0001', 'c8ec0001', 'd0e40001', 'd8f43c00', 'd8e44000', 'd5e30001', 'a0d24000', '96cb4000', 'a7d34000', '9ce44000', 'd8d84000', 'cde24000', 'b0d64000', 'b4d94000', 'd5f04000', 'd8d24000', 'c0eb4000', 'c1ea4000', 'baea4000', '88ab4000', 'a6674000', '0fa74000', 'b68b4000', '54c24000', 'aab74000', '7dcd4000', 'af8a4000', '0ce54000', '1aa34000', '23694000', '18a74000']
        self.HEX_STRS = [[30, 0, 224, 220, 147, 69, 1, 200], [30, 0, 224, 236, 147, 69, 1, 200], [30, 0, 224, 228, 147, 69, 1, 208], [30, 60, 224, 244, 147, 69, 0, 216], [30, 64, 224, 228, 147, 69, 0, 216], [30, 0, 224, 227, 147, 69, 1, 213], [30, 64, 224, 210, 147, 69, 0, 160], [30, 64, 224, 203, 147, 69, 0, 150], [30, 64, 224, 211, 147, 69, 0, 167], [30, 64, 224, 228, 147, 69, 0, 156], [30, 64, 224, 216, 147, 69, 0, 216], [30, 64, 224, 226, 147, 69, 0, 205], [30, 64, 224, 214, 147, 69, 0, 176], [30, 64, 224, 217, 147, 69, 0, 180], [30, 64, 224, 240, 147, 69, 0, 213], [30, 64, 224, 210, 147, 69, 0, 216], [30, 64, 224, 235, 147, 69, 0, 192], [30, 64, 224, 234, 147, 69, 0, 193], [30, 64, 224, 234, 147, 69, 0, 186], [30, 64, 224, 171, 147, 69, 0, 136], [30, 64, 224, 103, 147, 69, 0, 166], [30, 64, 224, 167, 147, 69, 0, 15], [30, 64, 224, 139, 147, 69, 0, 182], [30, 64, 224, 194, 147, 69, 0, 84], [30, 64, 224, 183, 147, 69, 0, 170], [30, 64, 224, 205, 147, 69, 0, 125], [30, 64, 224, 138, 147, 69, 0, 175], [30, 64, 224, 229, 147, 69, 0, 12], [30, 64, 224, 163, 147, 69, 0, 26], [30, 64, 224, 105, 147, 69, 0, 35], [30, 64, 224, 167, 147, 69, 0, 24]]
        self.LEN      = 20

    def calculate(self, khronos: int or None = None):
        
        UT = khronos if khronos is not None else int(time.time())
        FC = random.randint(0, len(self.HASHES))
        HS = self.HEX_STRS[FC]
        HX = self.HASHES[FC]
        HL = self.__hash_list(UT)
        HK = self.__encryption_key(256, HS)
        HL = self.__xor_hash_list(HL, HK)
        HD = self.__handle_xor(HL)
        RS = "".join([self.__hex_str(HS) for HS in HD])

        return {
            "X-Gorgon": f"0404{HX}{RS}",
            "X-Khronos": str(UT),
        }

    def __hex_str(self, X: int) -> str:
        Y = self.__to_hex(X)
        return Y if len(Y) > 2 else "0" + Y

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

    def __hash_list(self, UT: int) -> str:
        HT = self.__to_hex(UT)
        MP = str(hashlib.md5(self.params.encode("utf-8")).hexdigest())
        RG = self.__calc_ranges(start=4)

        PHL = [self.__from_hex(MP[i * 2 : 2 * i + 2]) for i in RG]
        EHL = [0 for i in range(len(RG) * 3)]
        UHL = [self.__from_hex(HT[i * 2 : 2 * i + 2]) for i in RG]

        return PHL + EHL + UHL

    def __from_hex(self, hex: hex) -> int:
        return self.__convert_base(hex, int(16))

    def __convert_base(self, hex: str, base: int) -> int:
        return sum(
            self.DGTS[digit] * (base**i)
            for i, digit in enumerate(reversed(hex.lower()))
        )

    def __to_hex(self, num: int) -> hex:
        return format(int(num), "x")

    def __calc_ranges(self, start: int = 0, stop: None = None, step: int = 1) -> list:
        if stop is None:
            stop = start
            start = 0

        if ((step > 0) & (start >= stop)) or (step < 0) & (start <= stop):
            return []

        return [x for x in range(start, stop, step)]

    def __handle_xor(self, hash_list: list):

        HL = hash_list
        RG = self.__calc_ranges(self.LEN)

        for i in RG:
            A = HL[i]
            B = self.__reverse(A)
            C = int(HL[(i + 1) % self.LEN])
            D = B ^ C
            E = self.__hex_rbit(D)
            F = E ^ self.LEN
            G = ~F
            while G < 0:
                G += 4294967296

            a = self.__to_hex(G)
            offset = len(a) - 2

            H = self.__from_hex(self.__to_hex(G)[offset:])
            HL[i] = H

        return HL

    def __reverse(self, num):
        T = self.__to_hex(num)
        if len(T) < 2:
            T = "0" + T

        return self.__from_hex(T[1:10] + T[0:1])

    def __hex_rbit(self, X: int):
        BN = format(X, "b")

        while len(BN) < 8:
            BN = "0" + BN
        RS = "".join([BN[7 - i] for i in range(8)])

        return int(RS, 2)

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

    def __hex_max(self, val, max=256):
        while val >= 256:
            val = val - 256
        return val


if __name__ == "__main__":
    sig = Gorgon("x=123&y=332").calculate(1662759087)
    print(sig)
