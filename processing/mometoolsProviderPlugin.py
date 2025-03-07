from qgis.core import QgsApplication
from .mometoolsProvider import MometoolsProvider

class MometoolsProviderPlugin:
    def __init__(self):
        self.provider = MometoolsProvider()

    def initGui(self):
        QgsApplication.processingRegistry().addProvider(self.provider)
    
    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)