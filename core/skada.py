

class Skada(object):
    _skada = {}
    @classmethod
    def get(this):
        return this._skada

    @classmethod
    def init(this):
        this._skada = {}

    reset = init

    @classmethod
    def sum(this):
        def dmg(c):
            _sum = 0
            for i in c:
                _sum += c[i]
            return _sum

        for i in this._skada:
            print(i,'dmg:', dmg(this._skada[i]['dmg']) )
            print(i,'odmg:', dmg(this._skada[i]['odmg']) )





