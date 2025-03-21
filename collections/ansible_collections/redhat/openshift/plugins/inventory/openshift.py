# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: openshift
    author:
      - Chris Houseknecht (@chouseknecht)

    short_description: OpenShift inventory source

    description:
      - Fetch containers, services and routes for one or more clusters
      - Groups by cluster name, namespace, namespace_services, namespace_pods, namespace_routes, and labels
      - Uses openshift.(yml|yaml) YAML configuration file to set parameter values.

    deprecated:
      removed_in: 5.0.0
      why: |
        As discussed in U(https://github.com/ansible-collections/kubernetes.core/issues/31), we decided to
        remove the openshift inventory plugin in release 5.0.0.
      alternative: "Use M(kubernetes.core.k8s_info) and M(ansible.builtin.add_host) instead."

    options:
      plugin:
        description: token that ensures this is a source file for the 'openshift' plugin.
        required: True
        choices: ['openshift', 'redhat.openshift.openshift']
      connections:
          description:
          - Optional list of cluster connection settings. If no connections are provided, the default
            I(~/.kube/config) and active context will be used, and objects will be returned for all namespaces
            the active user is authorized to access.
          suboptions:
              name:
                  description:
                  - Optional name to assign to the cluster. If not provided, a name is constructed from the server
                    and port.
              kubeconfig:
                  description:
                  - Path to an existing Kubernetes config file. If not provided, and no other connection
                    options are provided, the Kubernetes client will attempt to load the default
                    configuration file from I(~/.kube/config). Can also be specified via K8S_AUTH_KUBECONFIG
                    environment variable.
              context:
                  description:
                  - The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT environment
                    variable.
              host:
                  description:
                  - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.
              api_key:
                  description:
                  - Token used to authenticate with the API. Can also be specified via K8S_AUTH_API_KEY environment
                    variable.
              username:
                  description:
                  - Provide a username for authenticating with the API. Can also be specified via K8S_AUTH_USERNAME
                    environment variable.
              password:
                  description:
                  - Provide a password for authenticating with the API. Can also be specified via K8S_AUTH_PASSWORD
                    environment variable.
              client_cert:
                  description:
                  - Path to a certificate used to authenticate with the API. Can also be specified via K8S_AUTH_CERT_FILE
                    environment variable.
                  aliases: [ cert_file ]
              client_key:
                  description:
                  - Path to a key file used to authenticate with the API. Can also be specified via K8S_AUTH_KEY_FILE
                    environment variable.
                  aliases: [ key_file ]
              ca_cert:
                  description:
                  - Path to a CA certificate used to authenticate with the API. Can also be specified via
                    K8S_AUTH_SSL_CA_CERT environment variable.
                  aliases: [ ssl_ca_cert ]
              validate_certs:
                  description:
                  - "Whether or not to verify the API server's SSL certificates. Can also be specified via
                    K8S_AUTH_VERIFY_SSL environment variable."
                  type: bool
                  aliases: [ verify_ssl ]
              namespaces:
                  description:
                  - List of namespaces. If not specified, will fetch all containers for all namespaces user is authorized
                    to access.

    requirements:
    - "python >= 3.6"
    - "kubernetes >= 12.0.0"
    - "PyYAML >= 3.11"
"""

EXAMPLES = """
# File must be named openshift.yaml or openshift.yml

- name: Authenticate with token, and return all pods and services for all namespaces
  plugin: redhat.openshift.openshift
  connections:
    - host: https://192.168.64.4:8443
      api_key: xxxxxxxxxxxxxxxx
      verify_ssl: false

- name: Use default config (~/.kube/config) file and active context, and return objects for a specific namespace
  plugin: redhat.openshift.openshift
  connections:
    - namespaces:
        - testing

- name: Use a custom config file, and a specific context.
  plugin: redhat.openshift.openshift
  connections:
    - kubeconfig: /path/to/config
      context: 'awx/192-168-64-4:8443/developer'
"""

try:
    from ansible_collections.kubernetes.core.plugins.inventory.k8s import (
        K8sInventoryException,
        InventoryModule as K8sInventoryModule,
        format_dynamic_api_exc,
    )
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.client import (
        get_api_client,
    )

    HAS_KUBERNETES_COLLECTION = True
except ImportError as e:
    HAS_KUBERNETES_COLLECTION = False


try:
    from kubernetes.dynamic.exceptions import DynamicApiError
except ImportError:
    pass


class InventoryModule(K8sInventoryModule):
    NAME = "redhat.openshift.openshift"

    connection_plugin = "redhat.openshift.oc"
    transport = "oc"

    def check_kubernetes_collection(self):
        if not HAS_KUBERNETES_COLLECTION:
            raise K8sInventoryException(
                "The kubernetes.core collection must be installed"
            )

    def fetch_objects(self, connections):
        self.check_kubernetes_collection()
        super(InventoryModule, self).fetch_objects(connections)

        self.display.deprecated(
            "The 'openshift' inventory plugin has been deprecated and will be removed in release 5.0.0",
            version="5.0.0",
            collection_name="redhat.openshift",
        )

        if connections:
            if not isinstance(connections, list):
                raise K8sInventoryException("Expecting connections to be a list.")

            for connection in connections:
                client = get_api_client(**connection)
                name = connection.get(
                    "name", self.get_default_host_name(client.configuration.host)
                )
                if connection.get("namespaces"):
                    namespaces = connection["namespaces"]
                else:
                    namespaces = self.get_available_namespaces(client)
                for namespace in namespaces:
                    self.get_routes_for_namespace(client, name, namespace)
        else:
            client = get_api_client()
            name = self.get_default_host_name(client.configuration.host)
            namespaces = self.get_available_namespaces(client)
            for namespace in namespaces:
                self.get_routes_for_namespace(client, name, namespace)

    def get_routes_for_namespace(self, client, name, namespace):
        self.check_kubernetes_collection()
        v1_route = client.resources.get(
            api_version="route.openshift.io/v1", kind="Route"
        )
        try:
            obj = v1_route.get(namespace=namespace)
        except DynamicApiError as exc:
            self.display.debug(exc)
            raise K8sInventoryException(
                "Error fetching Routes list: %s" % format_dynamic_api_exc(exc)
            )

        namespace_group = "namespace_{0}".format(namespace)
        namespace_routes_group = "{0}_routes".format(namespace_group)

        self.inventory.add_group(name)
        self.inventory.add_group(namespace_group)
        self.inventory.add_child(name, namespace_group)
        self.inventory.add_group(namespace_routes_group)
        self.inventory.add_child(namespace_group, namespace_routes_group)
        for route in obj.items:
            route_name = route.metadata.name
            route_annotations = (
                {}
                if not route.metadata.annotations
                else dict(route.metadata.annotations)
            )

            self.inventory.add_host(route_name)

            if route.metadata.labels:
                # create a group for each label_value
                for key, value in route.metadata.labels:
                    group_name = "label_{0}_{1}".format(key, value)
                    self.inventory.add_group(group_name)
                    self.inventory.add_child(group_name, route_name)
                route_labels = dict(route.metadata.labels)
            else:
                route_labels = {}

            self.inventory.add_child(namespace_routes_group, route_name)

            # add hostvars
            self.inventory.set_variable(route_name, "labels", route_labels)
            self.inventory.set_variable(route_name, "annotations", route_annotations)
            self.inventory.set_variable(
                route_name, "cluster_name", route.metadata.clusterName
            )
            self.inventory.set_variable(route_name, "object_type", "route")
            self.inventory.set_variable(
                route_name, "self_link", route.metadata.selfLink
            )
            self.inventory.set_variable(
                route_name, "resource_version", route.metadata.resourceVersion
            )
            self.inventory.set_variable(route_name, "uid", route.metadata.uid)

            if route.spec.host:
                self.inventory.set_variable(route_name, "host", route.spec.host)

            if route.spec.path:
                self.inventory.set_variable(route_name, "path", route.spec.path)

            if hasattr(route.spec.port, "targetPort") and route.spec.port.targetPort:
                self.inventory.set_variable(route_name, "port", dict(route.spec.port))
