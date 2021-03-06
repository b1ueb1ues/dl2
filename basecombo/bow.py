conf = {

'xtype' : 'ranged'

, 'x1.idx'             : 1
, 'x1.hit'             : [(0.366, 'h1')]
, 'x1.attr.h1.coef'    : 0.29
, 'x1.attr.h1.missile' : [0, 0, 0]
, 'x1.sp'              : 184
, 'x1.stop'            : 0.433

, 'x2.idx'             : 2
, 'x2.hit'             : [(0.273, 'h1'), (0.485, 'h1')]
, 'x2.attr.h1.coef'    : 0.37
, 'x2.sp'              : 92
, 'x2.stop'            : 0.545

, 'x3.idx'             : 3
, 'x3.hit'             : [(0.485, 'h1')]
, 'x3.attr.h1.coef'    : 0.42
, 'x3.attr.h1.missile' : [0, 0, 0]
, 'x3.sp'              : 276
, 'x3.stop'            : 0.909

, 'x4.idx'             : 4
, 'x4.hit'             : [(0.278, 'h1'), (0.444, 'h1')]
, 'x4.attr.h1.coef'    : 0.63
, 'x4.sp'              : 414
, 'x4.stop'            : 0.556

, 'x5.idx'             : 5
, 'x5.hit'             : [(0.972, 'h1')]
, 'x5.attr.h1.coef'    : 0.35
, 'x5.attr.h1.to_bk'   : 3
, 'x5.attr.h1.missile' : [0, 0, 0, 0, 0]
, 'x5.sp'              : 529
, 'x5.stop'            : 1.389

# fs delay 0.5 0.633 ...
, 'fs.hit'             : [(0.333, 'h1')]
, 'fs.attr.h1.coef'    : 0.31
, 'fs.attr.h1.missile' : [0.5+0.133*0,
                          0.5+0.133*1,
                          0.5+0.133*2,
                          0.5+0.133*3,
                          0.5+0.133*4,
                          0.5+0.133*5,
                          0.5+0.133*6,
                          0.5+0.133*7]
, 'fs.sp'              : 460
, 'fs.marker'          : 0.350
, 'fs.stop'            : 1.0

, 'fsf.marker'         : 0.150
, 'fsf.stop'           : 0.333

, 'x1fs.marker'        : 0.42+0.350-0.366
}
