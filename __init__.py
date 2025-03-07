def classFactory(iface):
    from provider import Provider
    return Provider(iface)