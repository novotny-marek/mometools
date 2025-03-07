from qgis.core import QgsProcessingProvider
from .qgisUtils import gdf_to_qgis_layer, qgis_layer_to_gdf

class MometoolsProvider(QgsProcessingProvider):
    """
    The provider class of the plugin.
    """
    def loadAlgorithms(self):
        """
        Load algorithms into the provider.
        """
        self.addAlgorithm(gdf_to_qgis_layer())

    def id(self) -> str:
        """
        The id of the plugin.
        """
        return "mome_tools"
    
    def name(self):
        """
        The human friendly name of the plugin.
        """
        return self.tr("MomeTools")