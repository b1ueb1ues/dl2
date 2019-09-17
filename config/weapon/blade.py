conf = {

'xtype' : 'melee'

, 'x1.hit'          : [(0.17, 'h1')]
, 'x1.attr.h1.coef' : 0.97
, 'x1.sp'           : 130
, 'x1.recovery'     : 0.57

, 'x2.hit'          : [(0, 'h1')]
, 'x2.attr.h1.coef' : 0.97
, 'x2.sp'           : 130
, 'x2.recovery'     : 0.69

, 'x3.hit'          : [(0, 'h1'), (0.09, 'h1')]
, 'x3.attr.h1.coef' : 0.63
, 'x3.sp'           : 220
, 'x3.recovery'     : 0.70

, 'x4.hit'          : [(0, 'h1')]
, 'x4.attr.h1.coef' : 1.29
, 'x4.sp'           : 360
, 'x4.recovery'     : 0.91
, 'x4.cancel_by'    : ['s','fs']

, 'x5.hit'          : [(0, 'h1')]
, 'x5.attr.h1.coef' : 1.94
, 'x5.sp'           : 660
, 'x5.recovery'     : 1.29

, 'fsf.startup'     : 0          #?
, 'fsf.recovery'    : 33/60.0    #?

, 'fs.hit'          : [(0, 'h1')]
, 'fs.attr.h1.coef' : 0.92
, 'fs.sp'           : 200
, 'fs.startup'      : 30/60.0
, 'fs.recovery'     : 41/60.0

}
