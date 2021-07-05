import logging

from docker.errors import APIError, NotFound

logger = logging.getLogger('clients.docker.network')

class DockerNetworksMixin:

    def create_network(self, name):
        return self.client.networks.create(name, driver="bridge")

    def remove_network(self, network):
        try:
            network.remove()
        except APIError:
            logger.error("Error removing network %s", network.id)

    def get_network_by_id(self, network_id, verbose=False):
        try:
            return self.client.networks.get(network_id, verbose=verbose)
        except NotFound:
            logger.error("Network %s does not exists.", network_id)
            return None
        except APIError:
            logger.error("Error getting network %s", network_id)

    def connect_container_to_network(self, network, container):
        try:
            network.connect(container)
        except Exception:
            logger.error("Error connecting container %s with network %s", container, network.name)

    def disconnect_container_to_network(self, network, container, force=False):
        try:
            network.disconnect(container, force=force)
        except APIError:
            logger.error("Error 'detaching' container %s of network %s", container, network.name)

    def list_networks(self):
        try:
            return self.client.networks.list()
        except APIError:
            logger.error("Error listing networks")

    def networks_prune(self, filters=None):
        try:
            return self.client.networks.prune(filters=filters)
        except APIError:
            logger.error("Error prune networks")
