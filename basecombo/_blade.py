conf = {

'xtype' : 'melee'

, 'x1.idx'          : 1
, 'x1.hit'          : [(0.183, 'h1')]
, 'x1.attr.h1.coef' : 0.97
, 'x1.sp'           : 130
, 'x1.recovery'     : 0.364

, 'x2.idx'          : 2
, 'x2.hit'          : [(0.200, 'h1')]
, 'x2.attr.h1.coef' : 0.97
, 'x2.sp'           : 130
, 'x2.recovery'     : 0.364

, 'x3.idx'          : 3
, 'x3.hit'          : [(0.530, 'h1'), (0.606, 'h1')]
, 'x3.attr.h1.coef' : 0.63
, 'x3.sp'           : 220
, 'x3.recovery'     : 0.788

, 'x4.idx'          : 4
, 'x4.hit'          : [(0.433, 'h1')]
, 'x4.attr.h1.coef' : 1.29
, 'x4.sp'           : 360
, 'x4.recovery'     : 1.000
, 'x4.cancel_by'    : ['s','fs']

, 'x5.idx'          : 5
, 'x5.hit'          : [(0.349, 'h1')]
, 'x5.attr.h1.coef' : 1.94
, 'x5.sp'           : 660
, 'x5.recovery'     : 1.587

, 'fsf.startup'     : 0.76 # 0.62 my best
, 'fsf.recovery'    : 0

, 'fs.startup'      : 0.37  # 0.15 from datamined
, 'fs.hit'          : [(0.133, 'h1')]
, 'fs.attr.h1.coef' : 0.92
, 'fs.attr.h1.to_bk': 6
, 'fs.sp'           : 200
, 'fs.recovery'     : 0.833

, 'x1fs.startup'    : 0.68

}
