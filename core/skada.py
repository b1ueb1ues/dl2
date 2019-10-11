

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

        r = {}
        for i in this._skada:
            d = dmg(this._skada[i]['dmg'])
            od = dmg(this._skada[i]['odmg'])
            r[i] = {'dmg':d, 'odmg':od}
            print(i,' dmg:', d )
            print(i,'odmg:', od )
        return r





