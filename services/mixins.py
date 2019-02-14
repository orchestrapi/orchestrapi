class LoadBalancerMixin:

    def update_conf(self, app):
        config_file = self.main_config_file
        if not config_file:
            return
        config_file.update_container_ips(app)
        if not self.is_running():
            self.run()
        if self.container_id:
            if not self.networks.all().exists():
                self.networks.add(app.project.network)
            self.dclient.get_container_by_name(self.container_id).restart()
