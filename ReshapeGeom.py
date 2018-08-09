# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit, QAction, QIcon, QMessageBox
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer, QgsExpressionContextUtils, QgsExpressionContextScope, QgsFeatureRequest
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMessageBar
import resources_rc

class ReshapeGeom():
    

    def __init__(self, iface):

        self.iface = iface
		
    def initGui(self): 

        self.layer = self.iface.activeLayer()
        
        # Criação da action e da toolbar
        self.toolbar = self.iface.addToolBar("My_ToolBar")
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/ReshapeGeom/icon.png'
        self.action = QAction (QIcon (icon_path),u"ReshapeGeom.", pai)
        self.action.setObjectName ("ReshapeGeom.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)
        self.isEditing = 0

        if self.layer:
            self.iface.activeLayer().featureAdded.connect(self.run) # Sinal que chama a função e retorna o 'id'.
        else:
            pass
  

    def unload(self):

        del self.toolbar
        

    # def unChecked(self):

    #     self.action.setCheckable(False)
    #     self.action.setCheckable(True)
     

    def run(self,fid): # recebendo  id da funcao
        
        for feature in polygonpr.getFeatures():
            geometry = QgsGeometry.fromPolygon(feature.geometry().asPolygon())
            for line in linepr.getFeatures():
                t = feature.geometry().reshapeGeometry(line.geometry().asPolyline())   
                print t
        



