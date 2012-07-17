# -*- coding: utf-8 -*-
from Tkinter import *
import random,os,time,urllib,pickle



class App(Frame):
    tvary = ['A','A','B','B','C','C','D','D','E','E','F','F','G','G','H','H','I','I','J','J',
             'K','K','L','L','M','M','N','N','O','O','P','P','Q','Q','R','R','S','S','T','T',
             'U','U','V','V','W','W','X','X','Y','Y','Z','Z'
             'AA','AA','BB','BB','CC','CC','DD','DD','EE','EE','FF','FF','GG','GG']
        
        

    def __init__(self,master):
        Frame.__init__(self,master)
        self.master.title("Pexeso")
    
        self.grid()
        
        self.menu = Menu(self)
        self.master.config(menu=self.menu)
        self.menuHra = Menu(self.menu)
        self.menuHelp = Menu(self.menu)       

        self.menu.add_cascade(label="Hra",menu=self.menuHra)
        self.menuHra.add_command(label="Nová hra",command=self.novahra)
        self.menuHra.add_command(label="Nastavení",command=self.settings)
        self.menuHra.add_command(label="Nejlepší skóre",command=self.hightscore)
        self.menuHra.add_separator()
        self.menuHra.add_command(label="Konec hry",command=master.destroy)

        self.menu.add_cascade(label="Nápověda",menu=self.menuHelp)
        self.menuHelp.add_command(label="O pragramu",command=self.oprogramu)
        self.menuHelp.add_command(label="Jak hrát",command=self.helper)

        self.otocenych = 0
        self.uhadnutych = 0
        
        self.casswitch = 0
        self.cfg = {}
        
        f = open('hightscore.txt','r')
        self.high = pickle.load(f)
        f.close()
        
        self.config()
        self.hrarun = 0
        
        
        self.main = Frame(master)
        self.main.grid()
    
        
        
    def vycisti(self):
        self.main.destroy()
        self.main = Frame(self.master)
        self.main.grid()        
        
        
    def config(self):
        if not os.path.exists("config.txt"):
            self.sconfigtxt = file("config.txt","w")
            text = u"config;username=user;gamex=6;gamey=6"
            self.sconfigtxt.write(text)
            self.sconfigtxt.close()

        if not os.path.exists("hightscore.txt"):
            self.shightscore = file("hightscore.txt","w")
            text = u"hightscore;"
            self.shightscore.write(text)
            self.shightscore.close()

        soubor = file("config.txt","r")
        self.configtext = soubor.read()
        soubor.close()

        soubor = file("hightscore.txt","r")
        self.hightscore = soubor.read()
        soubor.close()

        
        config = self.configtext.split(';')
        
        for i in range(0,len(config)):
            sep = config[i].split('=')
            self.cfg[sep[0]] = sep[1]

        
           

       

    def clock(self):
        
        
        
        self.casovac.config(text = self.time)
        if self.casswitch == 1:
            self.time = self.time + 1
            self.main.after(1000, self.clock)
        else:
            self.time = 0

    def helper(self):
        self.oprog = Toplevel()
        text = Label(self.oprog,text=u"Pragam se ovládá pomocí myši")
        text2 = Label(self.oprog,text="Jednuduše klikejte na dvojice políček")
        text3 = Label(self.oprog,text="Po otočení dvou různých kartiček se vrátí zpět")
        text4 = Label(self.oprog,text="Pokud otočítě dvě stejné, zůstanou otočené")
        text5 = Label(self.oprog,text="Přeji hodně štěstí :)")
        text.grid(row = 1,pady=10,padx=5)
        text2.grid(row = 2,pady=10,padx=5)
        text3.grid(row = 3,pady=10,padx=5)
        text4.grid(row = 4,pady=10,padx=5)
        text5.grid(row = 5,pady=10,padx=5)

        self.tlkonec = Button(self.oprog,text="Zavřít",command=self.oprog.destroy)
        self.tlkonec.grid(row=6)
        

    def novahra(self):
        self.vycisti()
        self.nactiobrazky()
        self.radky = int(self.cfg['gamex'])
        self.sloupce = int(self.cfg['gamey'])
        self.vykreslyhru(self.radky,self.sloupce)
        self.vygenerujhru(self.radky,self.sloupce)
        self.casswitch = 1
        self.time = 0
        self.clock()
        
        
    
    def oprogramu(self):    
        self.oprog = Toplevel()
        text = Label(self.oprog,text=u"Program pexeso vytvořen roku 2012")
        text2 = Label(self.oprog,text="Vytvořil : Jan Horáček")
        text.grid(row = 1,pady=10,padx=5)
        text2.grid(row = 2,pady=10,padx=5)

    

                
    def hightscore(self):
        c=0
        self.whigh = Toplevel()
        gamename = self.high.keys()
        nadpis = Label(self.whigh,text="Hight score")
        psloup = 0
        for a in range(0,len(self.high)):
            if psloup >= 4:
                sloupec = 2
                if psloup == 4:
                    c = -4
            else:
                sloupec = 0
            psloup = psloup +1 
            helper = self.high[gamename[a]]
            nadpishry = Label(self.whigh,text = "Hra: " + gamename[a], font=("Helvetica", 16))
            nadpishry.grid(row = a+c,column = sloupec,padx = 10)
            pomoc = helper.keys()
            
            for b in range(0,len(pomoc)):
                
                cas = Label(self.whigh,text = str(pomoc[b]) + " s")
                jmeno = Label(self.whigh,text=helper[pomoc[b]])                
                jmeno.grid(row = a+c+1,column = sloupec,sticky="w",padx = 10)
                cas.grid(row = a+c+1,column = sloupec+1,padx = 10)
                c=c+1

    def controlhightscore(self):
        znakhra = str(self.cfg["gamex"]) + "*" + str(self.cfg["gamey"])
        hra = self.high[znakhra]
        self.time = 13
        casy = hra.keys()
        casy.append(self.time)
        
        intcasy = []
        for j in range(0,len(casy)):
            intcasy.append(int(casy[j]))
        intcasy.sort()
        
        highcopy = {}
        
        for k in range(0,len(intcasy)-1):
            if intcasy[k] == self.time:
                highcopy[intcasy[k]] = self.cfg["username"]
            else:
                highcopy[intcasy[k]] = self.high[znakhra][intcasy[k]]

        self.high[znakhra] = highcopy
        
        

        soubor = file("hightscore.txt","w")
        pickle.dump(self.high,soubor)
        soubor.close()
                
    

    def settings(self):
        self.wset = Toplevel(width = 200,height = 200)
        text = Label(self.wset,text="Roměr hry: ",anchor='w')
        self.rozmery = StringVar(self.wset)
        hrozmery = str(self.cfg["gamex"]) + "*" + str(self.cfg["gamey"])
        self.rozmery.set(hrozmery)
        option = OptionMenu(self.wset,self.rozmery,"4*5", "5*6", "6*6", "6*7","8*6", "8*8", "8*9")
        textname = Label(self.wset,text="Nick: ",anchor='w')
        self.username = StringVar(self.wset,value=self.cfg["username"])
        nickname = Entry(self.wset,textvariable=self.username,width = 9)
        submit = Button(self.wset,text = "Uložit",command=self.settingsuloz)

        text.grid(row = 0, column = 0,sticky = 'w',padx = 10,pady = 5)
        option.grid(row = 0,column = 1,sticky = 'w',padx = 10,pady = 5)
        textname.grid(row = 1,column = 0,sticky = 'w',padx = 10,pady = 5)
        nickname.grid(row = 1,column = 1,sticky = 'w',padx = 10,pady = 5)
        submit.grid(row = 2,columnspan = 2,pady = 10)
        
    def settingsuloz(self):
        rozmery = self.rozmery.get().split('*')
        self.cfg['gamex']=rozmery[0]
        self.cfg['gamey']=rozmery[1]
        jmeno = self.username.get()
        self.cfg['username']=jmeno

        txnewcfg = 'username='+jmeno+';gamex='+rozmery[0]+';gamey='+rozmery[1]
        sconfigtxt = file("config.txt","w")
        sconfigtxt.write(txnewcfg)
        sconfigtxt.close()
        
        self.wset.destroy()


    def nactiobrazky(self):
        pocet = (int(self.cfg["gamex"]) * int(self.cfg["gamey"]))
        
        self.photos = {}
        self.rszphotos = {}
        for i in range(0,pocet):
            if i%2 == 0:
                obrazurl = "img/" + self.tvary[i] + ".gif"
                self.photos[self.tvary[i]] = PhotoImage(file=obrazurl)
                self.rszphotos[self.tvary[i]] = self.photos[self.tvary[i]].subsample(2,2)
                
        
        

    def vykreslyhru(self,x,y):
        self.vyska = 100
        self.seznamTlacitek = []
        pocetRadku = x
        pocetSloupcu = y
        
        self.photo = PhotoImage(file ="img/back.gif")
        self.rszphoto = self.photo.subsample(2,2)
        for poradi in range(pocetRadku*pocetSloupcu):
            radek = poradi / pocetSloupcu
            sloupec = poradi % pocetSloupcu
            self.tlacitko = Button(self.main,text=str(poradi),width=self.vyska, height=self.vyska)
            self.tlacitko.bind("<Button-1>", self.otoc)
            
            self.tlacitko.config(image=self.rszphoto)
            self.tlacitko.grid(row=radek, column=sloupec)
            self.seznamTlacitek.append(self.tlacitko)
        self.casovactx = Label(self.main,text="časovač: ")
        self.casovactx.grid(row = self.radky+1)
        self.casovac = Label(self.main,text="0")
        self.casovac.grid(row = self.radky+1,column = 1)
    
    def otoc(self,event):
        
        tlacitko = event.widget
        cislotl = tlacitko.cget("text")
        znaktl = self.hra[int(cislotl)]
        
        if self.otocenych == 0:
            self.otocene1 = tlacitko
            self.otocenetx1 = tlacitko.cget("text")
            self.otocenych = self.otocenych +1
            self.otocenezn1 = znaktl
            
            tlacitko.config(image=self.rszphotos[znaktl])
            
        elif self.otocenych == 1:
            self.otocene2 = tlacitko
            self.otocenetx2 = tlacitko.cget("text")
            self.otocenych = self.otocenych +1
            self.otocenezn2 = znaktl

            tlacitko.config(image=self.rszphotos[znaktl])
        if self.otocenych == 2:
            if self.otocenezn1 == self.otocenezn2:
                self.otocenych = 0
                #self.otocene1.config(state = "disabled")
                self.otocene1.unbind("<Button-1>")
                #self.otocene2.config(state = "disabled")
                self.otocene2.unbind("<Button-1>")
                self.uhadnutych = self.uhadnutych + 1
                
            else:
                tlacitko.bind("<Leave>", self.otoczpet)
                self.otocenych = 0
        if self.uhadnutych == (self.radky*self.sloupce)/2:
            self.win()

        
        tlacitko.config(text= znaktl)
        
        
        
    def otoczpet(self,event):
        
        tlacitko = self.otocene1
        tlacitko.config(text = self.otocenetx1)
        tlacitko.config(image = self.rszphoto)
        tlacitko = self.otocene2
        tlacitko.config(text = self.otocenetx2)
        tlacitko.config(image = self.rszphoto)
        tlacitko.unbind("<Leave>")
      
    def vygenerujhru(self,x,y):
        self.hra = {}
        pocetznaku = (x*y)
        copy = list(self.tvary)

        for i in range(0,pocetznaku):
            randcislo = random.randint(0,pocetznaku-i-1)
            randcislo
            self.hra[i] = copy[randcislo]
            copy.pop(randcislo)
            
            
        

    def win(self):
        self.controlhightscore()
        self.winpanel = Toplevel()
        nadpis = Label(self.winpanel,text="Vítězství",font=("Helvetica", 24))
        cas = Label(self.winpanel,text="Váš dosažený čas: ")
        cass = Label(self.winpanel,text = str(self.time) + " s")
        newgame = Button(self.winpanel,text="Nová hra",command=self.winng)
        konec = Button(self.winpanel,text =" Konec",command=self.winend)
        nadpis.grid(row = 0,columnspan=3,pady=10)
        cas.grid(row = 1,padx=5)
        cass.grid(row = 1, column = 2)
        newgame.grid(row = 2,sticky="w",padx= 15,pady=15)
        konec.grid(row = 2, column = 2,padx=15,pady=15)
        print "winner"
        self.casswitch = 0
        self.time = 0
        self.uhadnutych = 0

    def winng(self):
        self.winpanel.destroy()
        self.novahra()
    def winend(self):
        self.winpanel.destroy()
        self.master.destroy()

if __name__=="__main__":

    root = Tk()
    app = App(root)
    root.mainloop()
