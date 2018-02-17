from Facturas import Factura
import os 
midir = os.path.dirname(os.path.realpath(__file__))


    

for archivo in os.listdir(midir):
    if ".xml" in archivo:

        f1 = Factura(os.path.join(midir,archivo))
        
        print f1.UUID
        print f1.version
        
        print f1.EmisorNombre
        print f1.EmisorRFC
        
        suma = 0
        for concepto in f1.conceptos:
            print concepto["descripcion"]
            suma += float(concepto["importeConcepto"])
             
        print "suma : " + str(suma)
         
         
        print "retencion IVA: "+str(f1.retenciones["IVA"])
        print "retencion ISR: "+str(f1.retenciones["ISR"])
        print "retencion ISH: "+str(f1.retenciones["ISH"])
        print "retencion IEPS: "+str(f1.retenciones["IEPS"])
        print "retencion TUA: "+str(f1.retenciones["TUA"])
         
        print "traslado IVA: importe = "+str(f1.traslados["IVA"]["importe"])+" tasa = "+str(f1.traslados["IVA"]["tasa"])
        print "traslado ISR: importe = "+str(f1.traslados["ISR"]["importe"])+" tasa = "+str(f1.traslados["ISR"]["tasa"])
        print "traslado ISH: importe = "+str(f1.traslados["ISH"]["importe"])+" tasa = "+str(f1.traslados["ISH"]["tasa"])
        print "traslado IEPS: importe = "+str(f1.traslados["IEPS"]["importe"])+" tasa = "+str(f1.traslados["IEPS"]["tasa"])
        print "traslado TUA: importe = "+str(f1.traslados["TUA"]["importe"])+" tasa = "+str(f1.traslados["TUA"]["tasa"])
         
        
        print "traslado local IVA: importe = "+str(f1.trasladosLocales["IVA"]["importe"])+" tasa = "+str(f1.trasladosLocales["IVA"]["tasa"])
        print "traslado local ISR: importe = "+str(f1.trasladosLocales["ISR"]["importe"])+" tasa = "+str(f1.trasladosLocales["ISR"]["tasa"])
        print "traslado local ISH: importe = "+str(f1.trasladosLocales["ISH"]["importe"])+" tasa = "+str(f1.trasladosLocales["ISH"]["tasa"])
        print "traslado local IEPS: importe = "+str(f1.trasladosLocales["IEPS"]["importe"])+" tasa = "+str(f1.trasladosLocales["IEPS"]["tasa"])
        print "traslado local TUA: importe = "+str(f1.trasladosLocales["TUA"]["importe"])+" tasa = "+str(f1.trasladosLocales["TUA"]["tasa"])
        
        print "retencion local IVA: importe = "+str(f1.retencionesLocales["IVA"]["importe"])+" tasa = "+str(f1.retencionesLocales["IVA"]["tasa"])
        print "retencion local ISR: importe = "+str(f1.retencionesLocales["ISR"]["importe"])+" tasa = "+str(f1.retencionesLocales["ISR"]["tasa"])
        print "retencion local ISH: importe = "+str(f1.retencionesLocales["ISH"]["importe"])+" tasa = "+str(f1.retencionesLocales["ISH"]["tasa"])
        print "retencion local IEPS: importe = "+str(f1.retencionesLocales["IEPS"]["importe"])+" tasa = "+str(f1.retencionesLocales["IEPS"]["tasa"])
        print "retencion local TUA: importe = "+str(f1.retencionesLocales["TUA"]["importe"])+" tasa = "+str(f1.retencionesLocales["TUA"]["tasa"])
        f1.conviertemeEnTex() 
        #for i in range(1,100000):
        #    print i)     
        print f1.conceptos
        f1.conviertemeEnPDF(midir)