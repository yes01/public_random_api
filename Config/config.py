
class Config(object):

    DEBUG = False


class DevelopmentConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
