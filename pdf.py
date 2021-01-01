from fpdf import FPDF
import os

# Script that creates Pdf File based on given attributes # some functions are reused therefore i defined them
# and named them by the role they take in the pdf file
# at the end i delete all the files in the temp directory 
def create_pdf(stocks,weights,yd,yr,perf):
    class PDF(FPDF):
        pass

    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf_w=210
    pdf_h=297
    def logo(self):
        self.image("./Logo.jpeg", x = 0, y = 0,w=40,h=40)
    logo(pdf)
    def title(self,text):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 48)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='C', txt=text, border=0)
    
    title(pdf,text="Your Portfolio")    

    def header(self,text):
        self.set_xy(5.0,30)
        self.set_font('Arial', 'B', 24)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='L', txt=text, border=0)
    
    header(pdf, "Your allocation")

    def stock(self,y,stock,x=5):
        text = stock
        self.set_xy(x,y)
        self.set_font('Arial', 'B',12)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='L', txt=text, border=0)

    def weight(self,y,weight,x=50):
        weight *= 100
        r_weight = round(weight,2)
        text = str(r_weight) + "%"
        self.set_xy(x,y)
        self.set_font('Arial', 'B',12)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='L', txt=text, border=0)    

    x = 5 
    y = 40
    for i in range (len(stocks)):
        stock(pdf,y=y,stock = stocks[i],x=x)
        weight(pdf,y=y,weight=weights[i],x=x+85)
        y = y +5
        if i == int(len(stocks)/2):
            maxy=y
            x = 105
            y=40
    
    
    def pie_all(self):
        self.image("./temp/port_alloc.png", x = 25 , y = maxy+20 ,w=150,h=85)

    def pie_cat(self):
        self.image("./temp/cat_alloc.png", x = 25 , y = (maxy+95) ,w=150,h=85)
    
    def pie_cat_alt(self):
        self.image("./temp/cat_alloc.png", x = 25 , y = (maxy+40) ,w=150,h=85)


    if len(stocks) < 20:
        pie_all(pdf)
        pie_cat(pdf)
    else:
        pie_cat_alt(pdf)
    pdf.add_page()
    logo(pdf)
    title(pdf,"Portfolio History")
    
    header(pdf,"5 Year Performance : " + str (perf) + " %")

    def years(self,y,year):
        text = str(year)
        self.set_xy(5.0,y)
        self.set_font('Arial', 'B',12)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='L', txt=text, border=0)

    def yields(self,y,yields):
        yields= str(yields.round(2))
        yields = yields.replace('[',"").replace(']',"")
        text = str(yields) + "%"
        self.set_xy(50,y)
        self.set_font('Arial', 'B',12)
        self.set_text_color(30, 85, 124)
        self.cell(w=210.0, h=40.0, align='L', txt=text, border=0) 

    
    
    y = 40
    for i in range (5):
        years(pdf,y,yr[i])
        yields(pdf,y,yd[i])
        y = y +5

    


    def history(self):
        self.image("./temp/history.png", x = 30, y = 100 ,w=150,h=80)
    
    history(pdf)

    pdf.output('Portfolio4You.pdf','F')
    
    for f in os.listdir("./temp/"):
        os.remove(os.path.join("./temp/", f))
    print("Done")