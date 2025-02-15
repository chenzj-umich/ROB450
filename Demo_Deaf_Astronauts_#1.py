from machine import Pin, Timer, PWM
import utime
led = Pin(25, Pin.OUT)

timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq = 3.5, mode = Timer.PERIODIC, callback = blink)

class PMOD_SSD:
    
    def __init__(self, CAT, AA, AB, AC, AD, AE, AF, AG):
        self.pwm = PWM(Pin(pwm), freq=200, duty_u16=32768)
        self.top = Pin(AD, Pin.OUT, Pin.PULL_DOWN)
        self.topRight = Pin(AE, Pin.OUT, Pin.PULL_DOWN)
        self.topLeft = Pin(AC, Pin.OUT, Pin.PULL_DOWN)
        self.mid = Pin(AG, Pin.OUT, Pin.PULL_DOWN)
        self.botRight = Pin(AF, Pin.OUT, Pin.PULL_DOWN)
        self.botLeft = Pin(AB, Pin.OUT, Pin.PULL_DOWN)
        self.bot = Pin(AA, Pin.OUT, Pin.PULL_DOWN)
        
        self.num = -1
        self.reset()
        
    def off(self):
        self.top.off()
        self.topRight.off()
        self.topLeft.off()
        self.mid.off()
        self.botRight.off()
        self.botLeft.off()
        self.bot.off()
        
        self.num = -1
    
    def reset(self):
        self.off()
        
        self.topNum = 0
        self.topRightNum = 0
        self.topLeftNum = 0
        self.midNum = 0
        self.botRightNum = 0
        self.botLeftNum = 0
        self.botNum = 0
        
    def on(self):
        self.top.value(self.topNum)
        self.topRight.value(self.topRightNum)
        self.topLeft.value(self.topLeftNum)
        self.mid.value(self.midNum)
        self.botRight.value(self.botRightNum)
        self.botLeft.value(self.botLeftNum)
        self.bot.value(self.botNum)
    
    def changeNum(self, num):
        self.reset()
        
        if(num == 1):            
            self.topRightNum = 1
            self.botRightNum = 1
            self.num = 1
            
        elif(num == 2):            
            self.topNum = 1
            self.topRightNum = 1
            self.midNum = 1
            self.botLeftNum = 1
            self.botNum = 1
            self.num = 2
            
        elif(num == 3):
            self.topNum = 1
            self.topRightNum = 1
            self.midNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 3
            
        elif(num == 4):     
            self.topLeftNum = 1
            self.midNum = 1
            self.topRightNum = 1
            self.botRightNum = 1
            self.num = 4
            
        elif(num == 5):
            self.topNum = 1
            self.topLeftNum = 1
            self.midNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 5
            
        elif(num == 6):
            self.topNum = 1
            self.topLeftNum = 1
            self.midNum = 1
            self.botLeftNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 6
            
        elif(num == 7):   
            self.topNum = 1
            self.topRightNum = 1
            self.botRightNum = 1
            self.num = 7
            
        elif(num == 8): 
            self.topNum = 1
            self.topLeftNum = 1
            self.topRightNum = 1
            self.midNum = 1
            self.botLeftNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 8
            
        elif(num == 9):
            self.topNum = 1
            self.topLeftNum = 1
            self.topRightNum = 1
            self.midNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 9
            
        elif(num == 0):
            self.topNum = 1
            self.topLeftNum = 1
            self.topRightNum = 1
            self.botLeftNum = 1
            self.botRightNum = 1
            self.botNum = 1
            self.num = 0
            
        self.on()
        
    def getNum(self):
        return self.num

class PMOD:
    def __init__(self, CAT, AA, AB, AC, AD, AE, AF, AG):
        self.pmodSSD_1 = PMOD_SSD(CAT, AA, AB, AC, AD, AE, AF, AG)
        self.pmodSSD_2 = PMOD_SSD(CAT, AA, AB, AC, AD, AE, AF, AG)
        
        self.interrupt_pin = Pin(16, Pin.IN)
        
        self.interrupt_pin.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=self.callback)
        
    def callback(self, interrupt_pin):
        if (self.interrupt_pin.value()):
            self.pmodSSD_2.off()
            self.pmodSSD_1.on()
        else:
            self.pmodSSD_1.off()
            self.pmodSSD_2.on()
            
    def changeNumber(self, num1, num2):
        self.pmodSSD_1.changeNum(num1)
        self.pmodSSD_2.changeNum(num2)
        
    def changeNumber1(self, num):
        self.pmodSSD_2.changeNum(num)
    
    def changeNumber2(self, num):
        self.pmodSSD_1.changeNum(num)
        
    def getNumber(self):
        return self.pmodSSD_1.getNum(), self.pmodSSD_2.getNum()

class AI:
    def __init__(self, inc, ent, pwm, bot, botLeft, topLeft, top, topRight, botRight, mid):
        self.inc = Pin(inc, Pin.IN, Pin.PULL_DOWN)
        self.ent = Pin(ent, Pin.IN, Pin.PULL_DOWN)
        
        self.pmod = PMOD(pwm, bot, botLeft, topLeft, top, topRight, botRight, mid)

        self.incNum = 0
        
        self.inc.irq(trigger=Pin.IRQ_RISING, handler=self.incNumber)
        self.ent.irq(trigger=Pin.IRQ_RISING, handler=self.entNumber)
        
        self.pmod.changeNumber(0, self.incNumber)

    def incNumber(self, inc):
        self.incNum += 1
        
        if (self.incNum > 9):
            self.incNum = 1
        
        self.pmod.changeNumber2(self.incNum)
        
    def entNumber(self, ent):
        if (self.incNum != 0):
            self.pmod.changeNumber(0,self.incNum)
            
            self.incNum = 0
    
    
if __name__ == '__main__':
    pwm = 6
    top = 10
    topRight = 9
    topLeft = 11
    mid = 7
    botRight = 8
    botLeft = 12
    bot = 13
    inc = 21
    ent = 19

    ai = AI(inc, ent, pwm, bot, botLeft, topLeft, top, topRight, botRight, mid)
    
    while True:
        continue