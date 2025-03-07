import geopandas as gpd
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry
from PyQt5.QtCore import QVariant

def qgis_layer_to_gdf(layer):
    """
    Converts QGIS layer to a GeoPandas GeoDataFrame.

    Parameters:
    layer (QgsVectorLayer): The QGIS Layer.

    Returns:
    gdf (gpd.GeoDataFrame): The GeoDataFrame converted from QGIS Layer
    """
    if not layer.isValid():
        raise ValueError("The provided QGIS layer is invalid.")
    
    features = list(layer.getFeatures())
    if not features:
        raise ValueError("The provided QGIS layer has no features.")
    
    crs = layer.crs().toWkt() if layer.crs().isValid() else None
    gdf = gpd.GeoDataFrame.from_features(features, crs=crs)

    return gdf


def gdf_to_qgis_layer(gdf, layer_name):
    """
    Converts a GeoPandas GeoDataFrame to a QGIS memory layer.

    Parameters:
    gdf (geopandas.GeoDataFrame): The GeoDataFrame containing the spatial data to be converted.
    layer_name (str): The name to be assigned to the new QGIS layer.

    Returns:
    QgsVectorLayer: The created QGIS vector layer.

    Raises:
    ValueError: If the geometry type of the GeoDataFrame is unsupported.

    The function performs the following steps:
    1. Determines the geometry type of the GeoDataFrame and maps it to a corresponding QGIS WKB type.
    2. Creates a QGIS memory layer with the appropriate geometry type and CRS.
    3. Adds the fields from the GeoDataFrame to the QGIS layer, mapping data types appropriately.
    4. Converts each feature in the GeoDataFrame to a QGIS feature and adds it to the QGIS layer.
    5. Updates the extents of the QGIS layer
    """
    # Determine geometry type for the layer
    geom_type = gdf.geometry.iloc[0].geom_type
    if geom_type in ['Point', 'MultiPoint']:
        wkb_type = 'Point'
    elif geom_type in ['LineString', 'MultiLineString']:
        wkb_type = 'LineString'
    elif geom_type in ['Polygon', 'MultiPolygon']:
        wkb_type = 'Polygon'
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")
    
    # Create memory layer
    crs_string = gdf.crs.to_string() if hasattr(gdf, 'crs') and gdf.crs else 'EPSG:4326'
    vector_layer = QgsVectorLayer(f"{wkb_type}?crs={crs_string}", layer_name, "memory")
    provider = vector_layer.dataProvider()
    
    # Add fields
    fields = []
    for col_name in gdf.columns:
        if col_name != 'geometry':
            dtype = gdf[col_name].dtype.name
            if dtype == 'int64':
                fields.append(QgsField(col_name, QVariant.Int))
            elif dtype in ['float64', 'float32']:
                fields.append(QgsField(col_name, QVariant.Double))
            elif dtype == 'bool':
                fields.append(QgsField(col_name, QVariant.Bool))
            else:
                fields.append(QgsField(col_name, QVariant.String))
    
    provider.addAttributes(fields)
    vector_layer.updateFields()
    
    # Add features
    features = []
    for idx, row in gdf.iterrows():
        feat = QgsFeature()
        
        # Convert shapely geometry to QGIS geometry
        wkt = row.geometry.wkt
        qgis_geom = QgsGeometry.fromWkt(wkt)
        feat.setGeometry(qgis_geom)
        
        # Set attributes (excluding geometry)
        attributes = []
        for col_name in gdf.columns:
            if col_name != 'geometry':
                attributes.append(row[col_name])
        
        feat.setAttributes(attributes)
        features.append(feat)
    
    provider.addFeatures(features)
    vector_layer.updateExtents()
    
    return vector_layer