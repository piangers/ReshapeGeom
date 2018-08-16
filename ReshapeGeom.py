# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit, QAction, QIcon
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer  
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool


class ReshapeGeom():
    

    def __init__(self, iface):
        self.iface = iface
		
    def initGui(self): 
		
        # cria uma ação que iniciará a configuração do plugin 
        self.initVariables()
        self.initSignals()
        
        
    def initVariables(self):
        # Criação da action e da toolbar
        self.toolbar = self.iface.addToolBar("Reshape")
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/ReshapeGeom/icon.png'
        self.action = QAction (QIcon (icon_path),u"Realiza o reshape de polígonos", pai)
        self.action.setObjectName ("ReshapeGeom")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)

        self.createRubberBand()
#        self.start()

    def createRubberBand(self):
        self.myRubberBand = QgsRubberBand( self.iface.mapCanvas() )
        color = QColor(78, 97, 114)
        color.setAlpha(190)
        self.myRubberBand.setColor(color)
        self.myRubberBand.setFillColor(QColor(255, 0, 0, 40))
        self.myRubberBand.setBorderColor(QColor(255, 0, 0, 200))

    def start(self):
        self.myRubberBand.reset()
        self.previousMapTool = self.iface.mapCanvas().mapTool()
        self.myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas() )
        self.isEditing = 0
        # Set MapTool
        self.iface.mapCanvas().setMapTool( self.myMapTool )
        self.iface.mapCanvas().xyCoordinates.connect( self.mouseMove )
        

    def initSignals(self):
        self.action.toggled.connect(self.initRubberBand)
        self.myMapTool.canvasClicked.connect( self.mouseClick )
        self.iface.mapCanvas().currentLayerChanged().connect(self.start)

    def initRubberBand(self, b):
        if b:
            self.start()
            
        else:
            self.disconnect()

    def disconnect(self):

        self.iface.mapCanvas().unsetMapTool(self.myMapTool)
        try:
            self.iface.mapCanvas().xyCoordinates.disconnect (self.mouseMove)
        except:
            pass

        try:
            self.myRubberBand.reset()
        except:
            pass

    def unload(self):
        self.disconnect()        

    def mouseClick( self, currentPos, clickedButton ):
        if self.iface.mapCanvas().currentLayer().type() != QgsMapLayer.VectorLayer:
            return
        else:
            if self.iface.mapCanvas().currentLayer().geometryType() != QGis.Polygon:
                return
            

        if clickedButton == Qt.LeftButton: 
            self.myRubberBand.addPoint( QgsPoint(currentPos) )
            self.isEditing = 1
            
        elif clickedButton == Qt.RightButton and self.myRubberBand.numberOfVertices() > 2:
            self.isEditing = 0
            
            layer = self.iface.mapCanvas().currentLayer()
	    layer.startEditing()
            line = self.myRubberBand.geometry()
            numInt = 0

           for feat in layer.getFeatures():
               geom = feat.geometry()
               if geom.intersects(line):
                   numInt = numInt + 1
                       geom.reshapeGeometry(line.asPolyline())
                       layer.changeGeometry(feat.id(), geom)

          if numInt == 0:
              print u'Linha de corte não intersecta nenhum polígono!'
          else:
              self.iface.mapCanvas().refresh()


    def mouseMove( self, currentPos ):
        if self.isEditing == 1:
            self.myRubberBand.movePoint( QgsPoint(currentPos) )



		
	
