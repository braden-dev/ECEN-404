# import math
import math
import sympy as sym
import matplotlib as plt

def parseEulerAngle(a):
    xRotation = a.split(" ")[1]
    yRotation = a.split(" ")[3]
    zRotation = a.split(" ")[4].split("]")[0]

    sym.init_printing()
    # x0,y0,z0,x1,y1,z1,xc,yc,zc,d1,r1,theta = sym.symbols('x0,y0,z0,x1,y1,z1,xc,yc,zc,d1,r1,theta')
    x0 = sym.Symbol('x0')
    y0 = sym.Symbol('y0')
    z0 = sym.Symbol('z0')
    x1 = sym.Symbol('x1')
    y1 = sym.Symbol('y1')
    z1 = sym.Symbol('z1')
    xc = sym.Symbol('xc')
    yc = sym.Symbol('yc')
    zc = sym.Symbol('zc')
    d1 = sym.Symbol('d1')
    r1 = sym.Symbol('r1')
    theta = sym.Symbol('theta')
    radius = sym.Symbol('radius')

    # X-Z Rotation
    # d1 = math.sqrt(math.pow((x1-x0),2) + math.pow((z1-z0),2))
    # r1 = math.sqrt(math.pow((xc-x1),2) + math.pow((zc-z1),2))
    # theta = math.acos(1 - math.pow(d1,2) / 2*math.pow(r1,2))
    
    # f = sym.Eq(math.sqrt((math.pow((x1-x0),2)) + math.pow((z1-z0),2)),d1)
    # g = sym.Eq(math.sqrt(math.pow((xc-x1),2) + math.pow((zc-z1),2)),r1)
    # h = sym.Eq(math.acos(1 - math.pow(d1,2) / 2*math.pow(r1,2)),theta)

    # Current Testing vv
    # # f = sym.Eq(pow((pow((x1-x0),2) + pow((z1-z0),2)),0.5),d1)
    # h = sym.Eq((pow((xc-x1),2) + pow((zc-z1),2)),(pow((xc-x0),2) + pow((zc-z0),2)))
    # # g = sym.Eq(sym.acos((1 - pow(d1,2) / (2*pow(r1,2)))),sym.cos((theta*sym.pi)/180))
    # g = sym.Eq((1 - ((pow((x1-x0),2) + pow((z1-z0),2)) / (2*pow(r1,2)))),sym.cos(theta))
    # # i = sym.Eq(pow((pow((xc-x0),2) + pow((zc-z0),2)),0.5),radius)


    h = sym.Eq((pow((34.5-x1),2) + pow((312.7-z1),2)),(pow((34.5-45),2) + pow((312.7-339.1),2)))
    g = sym.Eq((1 - ((pow((x1-45),2) + pow((z1-339.1),2)) / (2*pow(28.4114,2)))),sym.cos(-0.919764))

    # # #Test Example
    # # f = sym.Eq(pow((pow((x1-4),2) + pow((z1-2),2)),0.5),d1)
    # # h = sym.Eq(pow((pow((2-x1),2) + pow((2-z1),2)),0.5),r1)
    # # g = sym.Eq(sym.acos((1 - pow(d1,2) / (2*pow(r1,2)))),sym.cos((30*sym.pi)/180))

    answer = (sym.solve([h,g],(x1,z1),dict=True))
    print(answer)
    # print()
    # print(answer[0])
    # # print()
    # # print(answer[0][d1])

    # xC, zC = [], []
    # for theta in range(0,360):
    #     x = sym.Eq(((2**2*sym.cos(theta) - 2**2 + 4**2 - 4*2 + 2**2 - 2*2 + (-2 + 2)*(-2*pow((-(sym.cos(theta) - 1)*(2**2*sym.cos(theta) - 2**2 + 2*4**2 - 4*4*2 + 2*2**2 + 2*2**2 - 4*2*2 + 2*2**2)),0.5)*(4 - 2)/(4**2 - 2*4*2 + 2**2 + 2**2 - 2*2*2 + 2**2) + (2**2*2*sym.cos(theta) - 2**2*2 - 2**2*2*sym.cos(theta) + 2**2*2 + 4**2*2 - 2*4*2*2 + 2**2*2 + 2**3 - 2*2**2*2 + 2*2**2)/(4**2 - 2*4*2 + 2**2 + 2**2 - 2*2*2 + 2**2)))/(4 - 2)),x1)
    #     z = sym.Eq((-2*pow((-(sym.cos(theta) - 1)*(2**2*sym.cos(theta) - 2**2 + 2*4**2 - 4*4*2 + 2*2**2 + 2*2**2 - 4*2*2 + 2*2**2)),0.5)*(4 - 2)/(4**2 - 2*4*2 + 2**2 + 2**2 - 2*2*2 + 2**2) + (2**2*2*sym.cos(theta) - 2**2*2 - 2**2*2*sym.cos(theta) + 2**2*2 + 4**2*2 - 2*4*2*2 + 2**2*2 + 2**3 - 2*2**2*2 + 2*2**2)/(4**2 - 2*4*2 + 2**2 + 2**2 - 2*2*2 + 2**2)),z1)

    #     answerX1 = sym.solve([x],x1)
    #     answerZ1 = sym.solve([z],z1)

    #     xC.append(answerX1[x1])
    #     if(theta <= 180):
    #        diff = 2 - answerZ1[z1]
    #        answerZ1[z1] = 2 + diff

    #     zC.append(answerZ1[z1])



    # print(xC)
    # print(zC)

    # from matplotlib import pyplot as plt
    # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    # plt.xlim(0, 5)
    # plt.ylim(0, 5)
    # plt.grid()
    # plt.plot(xC, zC, marker="o", markersize=1, markeredgecolor="blue", markerfacecolor="blue")
    # plt.show()

    # X-Y Rotation


    # Y-Z Rotation

    # print(xRotation, yRotation, zRotation)

parseEulerAngle("[ 62.13945462  49.82242911 122.41165134]")