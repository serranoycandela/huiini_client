import wx
import wx.grid
import os
from Facturas import Factura
#import win32print
import win32api
import time as time_old
import jinja2
from subprocess import Popen




class MyImageRenderer(wx.grid.GridCellRenderer):
    def __init__(self, img):
        wx.grid.GridCellRenderer.__init__(self)
        self.img = img
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        
        dc.DrawBitmap(self.img, rect.X, rect.Y)
#         if isSelected:
#             grid.setselected(row, col, True)
#         else:
#             grid.SetSelectedStateOfItem(row, col, False)
        
    def Clone(self):
        return self.__class__()
#         image = wx.MemoryDC()
#         image.SelectObject(self.img)
#         dc.SetBackgroundMode(wx.SOLID)
#         if isSelected:
#             dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
#             dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
#         else:
#             dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
#             dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
# 
#         width, height = self.img.GetWidth(), self.img.GetHeight()
#       
#         dc.Blit(rect.x, rect.y, width, height, image, 0, 0, wx.COPY, True)

class GridFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(1000,500))
        self.midir = os.path.dirname(os.path.realpath(__file__))
        self.pdflatex_path = os.path.join(self.midir,"miktex\\bin\pdflatex.exe")
        
        
        
        
        panelArriba = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
        #panelAbajo = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(1000,200))
        #panelAbajo.SetMinSize((1000,200))

        
        carpetismo = wx.Panel(self,-1, style=wx.BORDER_NONE,size=(200,100))
        carpetismo.SetMinSize((200,100))
        #carpetismo.SetSize(0, 0, 400, 100, wx.SIZE_AUTO)
        btnCarpetismo = wx.Button(carpetismo, -1, "Escoje carpeta con CFDI", style=wx.ALIGN_CENTER_HORIZONTAL)
        btnCarpetismo.Bind(wx.EVT_BUTTON,self.OnClicked)
        
        pizarrin = wx.Panel(self,-1, style=wx.BORDER_NONE,size=(200,100))
        pizarrin.SetMinSize((200,100))
        #pizarrin.SetSize(0, 0, 400, 100, wx.SIZE_AUTO)
        self.pizarrinLabel = wx.StaticText(pizarrin, wx.ID_ANY, label="oo", style=wx.ALIGN_CENTER)

        impresion = wx.Panel(self,-1, style=wx.BORDER_NONE,size=(200,100))
        impresion.SetMinSize((200,100))
        #impresion.SetSize(0, 0, 400, 100, wx.SIZE_AUTO)
        btnImprime = wx.Button(impresion, -1, "Imprime")
        btnImprime.Bind(wx.EVT_BUTTON,self.imprime)
        btnCambia = wx.Button(impresion, -1, "Cambia Impresora")
        btnCambia.Bind(wx.EVT_BUTTON,self.OnClicked)
        boxImprime = wx.BoxSizer(wx.VERTICAL)
        boxImprime.Add(btnImprime, 1, wx.EXPAND)
        boxImprime.Add(btnCambia, 2, wx.EXPAND)
        
        impresion.SetAutoLayout(True)
        impresion.SetSizer(boxImprime)
        impresion.Layout()
        self.pizarrinLabel.SetLabel("puto el que lo lea")
        
        boxAbajo = wx.BoxSizer(wx.HORIZONTAL)
        boxAbajo.Add(carpetismo, 1, wx.EXPAND)
        boxAbajo.Add(pizarrin, 2, wx.EXPAND)
        boxAbajo.Add(impresion, 3, wx.EXPAND)
        
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(16, 16)
        self.grid.SetColLabelValue(0, "PDF")
        self.grid.SetColSize(0, 40)
        self.grid.SetColLabelValue(1, "Fecha")
        self.grid.SetColSize(1, 120)
        self.grid.SetColLabelValue(2, "UUID")
        self.grid.SetColSize(2, 80)
        self.grid.SetColLabelValue(3, "Nombre del Emisor")
        self.grid.SetColSize(3, 200)
        self.grid.SetColLabelValue(4, "RFC del Emisor")
        self.grid.SetColSize(4, 100)
        self.grid.SetColLabelValue(5, "Descripcion")
        self.grid.SetColSize(5, 200)
        self.grid.SetColLabelValue(6, "V")
        self.grid.SetColSize(6, 40)
        self.grid.SetColLabelValue(7, "Sub Total")
        self.grid.SetColSize(7, 100)
        self.grid.SetColLabelValue(8, "Descuento")
        self.grid.SetColSize(8, 80)
        self.grid.SetColLabelValue(9, "IVA")
        self.grid.SetColSize(9, 80)
        self.grid.SetColLabelValue(10, "IEPS")
        self.grid.SetColSize(10, 80)
        self.grid.SetColLabelValue(11, "Ret. IVA")
        self.grid.SetColSize(11, 80)
        self.grid.SetColLabelValue(12, "Ret. ISR")
        self.grid.SetColSize(12, 80)
        self.grid.SetColLabelValue(13, "Total")
        self.grid.SetColSize(13, 80)
        self.grid.SetColLabelValue(14, "Metodo de pago")
        self.grid.SetColSize(14, 140)
        self.grid.SetColLabelValue(15, "Forma de Pago")
        self.grid.SetColSize(15, 80)
    
        
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDClick)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelDClick)
        self.gridDiot = wx.grid.Grid(self, -1)

        self.gridDiot.CreateGrid(3, 8)
        self.gridDiot.SetColLabelValue(0, "PDF")
        self.gridDiot.SetColSize(0, 40)
        
        self.gridDiot.SetColLabelValue(1, "Sub Total")
        self.gridDiot.SetColSize(1, 100)
        self.gridDiot.SetColLabelValue(2, "Descuento")
        self.gridDiot.SetColSize(2, 80)
        self.gridDiot.SetColLabelValue(3, "IVA")
        self.gridDiot.SetColSize(3, 80)
        self.gridDiot.SetColLabelValue(4, "IEPS")
        self.gridDiot.SetColSize(4, 80)
        self.gridDiot.SetColLabelValue(5, "Ret. IVA")
        self.gridDiot.SetColSize(5, 80)
        self.gridDiot.SetColLabelValue(6, "Ret. ISR")
        self.gridDiot.SetColSize(6, 80)
        self.gridDiot.SetColLabelValue(7, "Total")
        self.gridDiot.SetColSize(7, 80)

        palomita = wx.Bitmap("palomita.png", wx.BITMAP_TYPE_PNG)
        self.palomitaRenderer = MyImageRenderer(palomita)
        tache = wx.Bitmap("x.png", wx.BITMAP_TYPE_PNG)
        self.tacheRenderer = MyImageRenderer(tache)
        
       
               
        box = wx.BoxSizer(wx.VERTICAL)
        
        box.Add(panelArriba, 1, wx.EXPAND)
        box.Add(self.grid, 2, wx.EXPAND)
        box.Add(self.gridDiot, 3, wx.EXPAND)
        box.Add(boxAbajo, 4, wx.EXPAND)
 
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout() 
        self.Fit()
        self.Show()
        
    def sumale(self, renglonResumen=0):
        for columna in range(7,14):
            suma = 0
            for renglon in range(len(self.listaDeFacturasOrdenadas)):
                if len(self.grid.GetCellValue(renglon, columna)) > 0 and self.grid.GetCellValue(renglon, columna) != 'None':       
                    suma += float(self.grid.GetCellValue(renglon, columna))
                
            self.gridDiot.SetCellValue(renglonResumen, columna-6, "{:.2f}".format(suma) )
            
        
#         if renglonResumen == 1:    
#             self.grid.SetCellValue(1,0,QTableWidgetItem("Resumen Diot Actualizado"))    
#             self.tableWidget_resumen.setItem(1,1,QTableWidgetItem("Sumatoria del Periodo Actualizada"))  
#             self.tableWidget_resumen.setCellWidget(1,2,ImgWidget1(self))
#             self.tableWidget_resumen.setCellWidget(0,2,ImgWidget2(self))
        
    def imprime(self,algo):
        #objetosMagicosOrdenados = sorted(self.objetosMagicos, key=lambda objetosMagicos: objetosMagicos.fecha)
        
        for factura in self.listaDeFacturasOrdenadas:
            print(factura.xml_path[:-3]+"pdf")
            try:
                
                if factura.total > 0:
                    print(factura.fechaTimbrado)
                    hh = win32api.ShellExecute(0, "print", factura.xml_path[:-3]+"pdf", None,  ".",  0)
                    if hh > 32:
                        print("algo")
                        time_old.sleep(10)
                
                elif factura.total < 0:
                    print("negativo?????")
                else:#si es cero
                    print("nada")
            except:
                print("hay un pdf faltante o corrupto")    
            
            
        #hh = win32api.ShellExecute(0, "print", os.path.join(self.esta_carpeta,"resumenDiot.pdf"), None,  ".",  0)
        
        
        
#         for esteFile in listdir(join(self.esteFolder, "pdfs/")):
#             if isfile(join(join(self.esteFolder, "pdfs/"), esteFile)):
#                 if esteFile[-3:] == "pdf":
#                     # print('"/usr/bin/lpr", ' + join(join(self.esteFolder, "pdfs/"), esteFile))
#                     p = subprocess.call(["C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe", "/N", "/T", join(join(self.esteFolder, "pdfs/"), esteFile)])
#         
        #C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader
        
    def getTemplate(self,tpl_path):
            path, filename = os.path.split(tpl_path)
            return jinja2.Environment(
                loader=jinja2.FileSystemLoader(path or './')
            ).get_template(filename)
        
        

    def hazResumenDiot(self):
        sumaSubTotal = 0
        sumaDescuento = 0
        sumaTrasladoIVA = 0
        sumaImporte = 0
        for key, value in self.diccionarioPorRFCs.items():
            sumaSubTotal += value['subTotal']
            sumaDescuento += value['descuento']
            sumaTrasladoIVA += value['trasladoIVA']
            sumaImporte += value['importe']
        
        self.listaDiot = []
        for key, value in self.diccionarioPorRFCs.items():
            self.listaDiot.append({'rfc' : key,
                                   'subTotal': value['subTotal'], 
                                   'descuento': value['descuento'], 
                                   'trasladoIVA': value['trasladoIVA'],
                                   'importe': value['importe']
                                    })
        
            
        self.listaDiot.append({'rfc' : 'Suma',
                               'subTotal': sumaSubTotal, 
                               'descuento': sumaDescuento, 
                               'trasladoIVA': sumaTrasladoIVA,
                               'importe': sumaImporte
                                })    
        
        
        
        for key, value in self.diccionarioPorRFCs.items():
            print(key, value)
        context = {'lista_diot': self.listaDiot}
        self.tex_path = os.path.join(self.esta_carpeta,"resumenDiot.tex")
        self.getTemplate("templateDiot.tex").stream(context).dump(self.tex_path)
        try:
            from subprocess import DEVNULL # Python 3
        except ImportError:
            DEVNULL = open(os.devnull, 'r+b', 0)
        
        #Popen([self.pdflatex_path, self.tex_path], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL) 
        print(self.pdflatex_path, self.tex_path)
        Popen([self.pdflatex_path, "-output-directory", self.esta_carpeta,self.tex_path]) 
        
    def OnDClick(self,algo):
        print("me picaron en : " +str(algo.GetCol()))
        column = algo.GetCol()
        row = algo.GetRow()
        if column == 2:
              
             
            xml = os.path.join(self.esta_carpeta,self.grid.GetCellValue(row,2)+".xml")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                os.startfile(xml)
                print("este guey me pico:"+xml)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir xmls")
                #QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicacion por default para abrir xmls" )  
                  
        if column == 0:
              
            pdf = os.path.join(self.esta_carpeta,self.grid.GetCellValue(row,2)+".pdf")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                print("este guey me pico:"+pdf)
                os.startfile(pdf)
                
            except:
                print ("el sistema no tiene una aplicacion por default para abrir pdfs")
                #QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicacion por default para abrir pdfs" ) 
        
    def OnLabelDClick(self,algo):
        print("me doble picaron y soy columna")
    def OnClicked(self, event): 
        dialog = wx.DirDialog(None, "Choose a directory :", style=1 ) 
        if dialog.ShowModal() == wx.ID_OK: 
            self.esta_carpeta = dialog.GetPath() 
        dialog.Destroy() 
        self.pizarrinLabel.SetLabel(self.esta_carpeta)
        self.listaDeFacturas = []
        for archivo in os.listdir(self.esta_carpeta):
            if ".xml" in archivo:
        
                self.listaDeFacturas.append(Factura(os.path.join(self.esta_carpeta,archivo)))
            
        
        self.listaDeFacturasOrdenadas = sorted(self.listaDeFacturas, key=lambda listaDeFacturas: listaDeFacturas.fechaTimbrado)
        self.diccionarioPorRFCs = {}
        
        contador = 0
        for factura in self.listaDeFacturasOrdenadas:
            factura.conviertemeEnTex() 
            factura.conviertemeEnPDF(self.esta_carpeta)
            self.grid.SetReadOnly(contador, 0, isReadOnly=True)
            self.grid.SetCellRenderer(contador,0,self.palomitaRenderer)
            #self.grid.SetCellValue(contador, 0, icono)
            self.grid.SetCellValue(contador, 1, factura.fechaTimbrado)
            self.grid.SetCellValue(contador, 2, factura.UUID)
            self.grid.SetCellValue(contador, 3, factura.ReceptorNombre)
            self.grid.SetCellValue(contador, 4, factura.EmisorRFC)
            self.grid.SetCellValue(contador, 5, factura.conceptos[0]["descripcion"])
            self.grid.SetCellValue(contador, 6, factura.version) 
            self.grid.SetCellValue(contador, 7, str(factura.subTotal))
            self.grid.SetCellValue(contador, 8, str(factura.descuento))
            
            self.grid.SetCellValue(contador, 9, str(factura.traslados["IVA"]["importe"]))
            self.grid.SetCellValue(contador, 10, str(factura.traslados["IEPS"]["importe"]))
            self.grid.SetCellValue(contador, 11, str(factura.retenciones["IVA"]))
            self.grid.SetCellValue(contador, 12, str(factura.retenciones["ISR"]))
            
            self.grid.SetCellValue(contador, 13, str(factura.total))
            self.grid.SetCellValue(contador, 14, str(factura.formaDePago))
            self.grid.SetCellValue(contador, 15, str(factura.metodoDePago))
            
            if factura.EmisorRFC in self.diccionarioPorRFCs:
                self.diccionarioPorRFCs[factura.EmisorRFC]['subTotal'] += float(factura.subTotal)
                self.diccionarioPorRFCs[factura.EmisorRFC]['descuento'] += float(factura.descuento)
                self.diccionarioPorRFCs[factura.EmisorRFC]['trasladoIVA'] += float(factura.traslados['IVA']['importe'])
                self.diccionarioPorRFCs[factura.EmisorRFC]['importe'] += float(factura.subTotal)-float(factura.descuento)
                print("sumale " + str(factura.subTotal) )
            else:
                self.diccionarioPorRFCs[factura.EmisorRFC] = {'subTotal': float(factura.subTotal), 
                                                              'descuento': float(factura.descuento), 
                                                              'trasladoIVA': float(factura.traslados['IVA']['importe']),
                                                              'importe': float(factura.subTotal)-float(factura.descuento)
                                                            }
                print("crealo con " + str(factura.subTotal))
            
                                    
            
            contador +=1
        
 
        self.sumale()    
        self.hazResumenDiot()
             
    #{'GSO080328MY5': {'subTotal': 58999.95, 'descuento': 818.5066, 'trasladoIVA': 0.0, 'importe': 58181.4434}, 
    # 'AMH080702RMA': {'subTotal': 4130.05, 'descuento': 0.0, 'trasladoIVA': 660.81, 'importe': 4130.05} 
    # }      
    #falta Descuento
  
   
if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()