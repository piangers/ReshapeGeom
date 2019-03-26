# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtWidgets import *
from OrganizaGrupo import resources_rc


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
        path = self.iface.mainWindow()
        icon_path = (':/plugins/ReshapeGeom/icon.png')
        self.action = QAction (QIcon (icon_path),u"Reshape feature.", path)
        self.action.setObjectName ("ReshapeGeom")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)

        self.lastButton = Qt.RightButton

        self.createRubberBand()
        self.start()

    def initSignals(self):
        self.action.toggled.connect(self.initRubberBand)
        self.myMapTool.canvasClicked.connect(self.mouseClick)
        self.iface.mapCanvas().currentLayerChanged.connect(self.start)

    def createRubberBand(self):
        self.myRubberBand = QgsRubberBand( self.iface.mapCanvas())
        color = QColor(78, 97, 114)
        color.setAlpha(190)
        self.myRubberBand.setColor(color)
        self.myRubberBand.setFillColor(QColor(255, 0, 0, 40))
        #self.myRubberBand.setBorderColor(QColor(255, 0, 0, 200))

    def start(self):
        self.myRubberBand.reset()
        self.previousMapTool = self.iface.mapCanvas().mapTool()
        self.myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas())
        self.isEditing = 0
        # Set MapTool
        self.iface.mapCanvas().setMapTool(self.myMapTool)
        self.iface.mapCanvas().xyCoordinates.connect( self.mouseMove)
        self.myMapTool.canvasClicked.connect(self.mouseClick)
        
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

    def mouseClick(self, currentPos, clickedButton):
        if self.iface.mapCanvas().currentLayer().type() != QgsMapLayer.VectorLayer:
            return
        else:
            if self.iface.mapCanvas().currentLayer().geometryType() != QgsWkbTypes.LineGeometry and self.iface.mapCanvas().currentLayer().geometryType() != QgsWkbTypes.PolygonGeometry : #
                return
        
        if clickedButton == Qt.LeftButton:
            if self.lastButton == Qt.RightButton:
                self.myRubberBand.reset()
            self.lastButton = Qt.LeftButton
            self.isEditing = 1          
        
        elif clickedButton == Qt.RightButton and self.myRubberBand.numberOfVertices() > 2:
            self.lastButton = Qt.RightButton
            self.doShape()

    def doShape(self):
        self.isEditing = 0
        layer = self.iface.mapCanvas().currentLayer() # layer atual.
        layer.startEditing() # Ligando a edição da layer.
        line = self.myRubberBand.asGeometry() # Linha do rubberband.
        
        for feat in layer.getFeatures():
            geom = feat.geometry() # geometria que receberá o reshape.
            if geom.intersects(line): # Se intersecta  
                geom.reshapeGeometry(QgsLineString(line.asPolyline()))# realiza o reshape entre a linha e a geometria.
                layer.changeGeometry(feat.id(), geom)
                self.iface.mapCanvas().refresh() # Refresh para atualizar, mas não salvar as alterações.

    def mouseMove( self, currentPos ): 
        if self.isEditing == 1:
          # self.myRubberBand.movePoint(QgsPoint(currentPos)) # Rubberband.
            self.myRubberBand.addPoint(QgsPointXY(currentPos)) # Freehand.


#https://github.com/JonathanWillitts/common-qgis-2-to-3-plugin-fixes
