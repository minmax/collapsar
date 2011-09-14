from collapsar.context import ApplicationContext
from collapsar.config.loaders import FSLoader


def get_context_from_yaml(file_name):
    from collapsar.config.yaml_config import YAMLConfig
    loader = FSLoader(file_name)
    config = YAMLConfig(loader)
    return ApplicationContext(config.get_descriptions())
