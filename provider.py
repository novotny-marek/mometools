from qgis.core import QgsProcessingProvider

class Provider(QgsProcessingProvider):
    """
    The provider class of the plugin.
    """
    def loadAlgorithms(self):
        """
        Load algorithms into the provider.
        """
        self.addAlgorithm()

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