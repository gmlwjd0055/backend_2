class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance
    def getBalance(self):
        return self.__balance
    def withdraw(self, amount):
        if amount > self.__balance:
            print("잔액 부족")
            return
        self.__balance -= amount


class PocketMon:
    def __init__(self, idx, name, hp, demage):
        self.idx = idx
        self.name = name
        self.hp = hp
        self.demage = demage

    def attack(self, other):
        other.hp = other.hp - self.demage
        print(self.name, "이 ", other.name, "를 공격했다.")

#상속 : 자식클래스(부모클래스), 부모 클래스에 있는 모든 걸 자식 클래스가 물려받는다.
class Pikachu(PocketMon):
    def speak(self):
        print("피카피카")
    def attack(self, other):
        print("백만볼트~!~!")
        super().attack(other) #부모에 있는 코드 호출
        #other.hp = other.hp - self.demage
        #print(self.name, "이 ", other.name, "를 전기공격했다.")

pikachu = Pikachu(25, "피카츄", 100, 10)
charizard = PocketMon(6, "리자몽", 300, 30)
print(charizard.hp)
pikachu.attack(charizard)
print(charizard.hp)