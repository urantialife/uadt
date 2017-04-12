"""
Usage: theater [-v] <scenario>
"""

import importlib
import sys
from docopt import docopt

from plugins import Plugin
from logger import LoggerMixin


class Theater(LoggerMixin):

    @property
    def plugins(self):
        """
        Returns a dictionary of plugins available.
        """

        return {
            plugin_class.identifier: plugin_class
            for plugin_class in Plugin.plugins
        }

    def get_plugin(self, identifier):
        """
        Returns a plugin class corresponding to the given identifier.
        """

        try:
            return self.plugins[identifier]
        except KeyError:
            self.error('Scenario "{0}" is not available'.format(identifier))

    def import_plugins(self):
        import scenarios

        # pylint: disable=broad-except
        for module in scenarios.__all__:
            try:
                module_id = "{0}.{1}".format('scenarios', module)
                importlib.import_module(module_id)
                self.debug(module_id + " loaded successfully.")
            except Exception as exc:
                self.warning(
                    "The scenarios.{0} module could not be loaded: {1} "
                    .format(module, str(exc)))
                self.log_exception()

    def main(self):
        arguments = docopt(__doc__, version='theater')
        self.setup_logging(level='debug' if arguments['-v'] else 'info')
        self.import_plugins()

        scenario_cls = self.get_plugin(arguments['<scenario>'])
        if scenario_cls is None:
            sys.exit(1)

        scenario = scenario_cls()
        self.info("Executing scenario: {0}".format(scenario.identifier))
        scenario.execute()


def main():
    theater = Theater()
    theater.main()

if __name__ == '__main__':
    main()
