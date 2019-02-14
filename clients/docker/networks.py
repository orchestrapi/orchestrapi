from docker.errors import NotFound, APIError


class DockerNetworksMixin:

    def create_network(self, name):
        return self.client.networks.create(name, driver="bridge")

    def remove_network(self, network):
        try:
            network.remove()
        except APIError:
            print(f"Error al eliminar la red {network.id}")

    def get_network_by_id(self, network_id, verbose=False):
        try:
            return self.client.networks.get(network_id, verbose=verbose)
        except NotFound:
            return None
        except APIError:
            print(f"Error obteniendo red {network_id}")

    def connect_container_to_network(self, network, container):
        try:
            network.connect(container)
        except Exception:
            print(
                f"Error conectando contenedor {container} a la red {network.name}")

    def disconnect_container_to_network(self, network, container, force=False):
        try:
            network.disconnect(container, force=force)
        except APIError:
            print(
                f"Error desconectando contenedor {container} a la red {network.name}")

    def list_networks(self):
        try:
            return self.client.networks.list()
        except APIError:
            print("Error al listar redes")

    def networks_prune(self, filters=None):
        try:
            return self.client.networks.prune(filters=filters)
        except APIError:
            print("Error borrando redes sin uso")
