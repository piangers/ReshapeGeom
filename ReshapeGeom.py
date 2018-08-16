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

    
        
  

    def unload(self):

        del self.toolbar
        

    def reshape(self,fid): # recebendo  id da funcao
        
        # Obter os objetos dataProvider para as camadas chamadas 'line' e 'buffer'
		linepr = QgsMapLayerRegistry.instance().mapLayersByName('line')[0].dataProvider()
		bufferpr = QgsMapLayerRegistry.instance().mapLayersByName('buffer')[0].dataProvider()

		# Cria uma camada de memória para armazenar o resultado
		resultl = QgsVectorLayer("Polygon", "result", "memory")
		resultpr = resultl.dataProvider()
		QgsMapLayerRegistry.instance().addMapLayer(resultl)


		for feature in bufferpr.getFeatures():
		# Salva a geometria original
			geometry = QgsGeometry.fromPolygon(feature.geometry().asPolygon())
			for line in linepr.getFeatures():
				# Cruza o polígono com a linha. Se eles se cruzarem, o recurso conterá uma metade da divisão
				t = feature.geometry().reshapeGeometry(line.geometry().asPolyline())
				if (t==0):
					# Cria um novo recurso para manter a outra metade da divisão
					diff = QgsFeature()
					# Calcular a diferença entre a geometria original e a primeira metade da divisão
					diff.setGeometry( geometry.difference(feature.geometry()))
					# Adicione as duas metades da divisão à camada de memória
					resultpr.addFeatures([feature])
					resultpr.addFeatures([diff])



