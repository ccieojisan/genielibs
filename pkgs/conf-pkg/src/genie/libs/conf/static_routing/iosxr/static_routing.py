"""
Implement IOSXR (iosxr) Specific Configurations for Static Route objects.
"""

# Table of contents:
#     class StaticRouting:
#         class DeviceAttributes:
#             class VrfAttributes:
#                 class AddressFamilyAttributes:
#                     class RouteAttributes:
#                         class InterfaceAttributes:
#                         class NextHopAttributes:

# Python
from abc import ABC
from netaddr import IPNetwork
# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

class StaticRouting(ABC):

    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            with configurations.submode_context(
                    attributes.format('router static', force=True)):
                # VrfAttributes
                for sub, attributes2 in attributes.mapping_values('vrf_attr',
                                                                  sort=True,
                                                                  keys=self.vrf_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                if apply:
                    if configurations:
                        self.device.configure(configurations)
                else:
                    return CliConfig(device=self.device, unconfig=unconfig,
                                     cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                vrf_context = ""
                if attributes.value('vrf') != 'default':
                    vrf_context = attributes.format('vrf {vrf}', force=True)

                with configurations.submode_context(vrf_context):
                    # AddressFamilyAttributes
                    for sub, attributes2 in attributes.mapping_values('address_family_attr',
                                                                      sort=True,
                                                                      keys=self.address_family_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                            attributes.format(('address-family {af} unicast')\
                                                      .format(af=attributes.value('af').value), force=True)):

                        for sub, attributes2 in attributes.mapping_values('route_attr',
                                                                          sort=True,
                                                                          keys=self.route_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                        if apply:
                            if configurations:
                                self.device.configure(configurations)
                        else:
                            return CliConfig(device=self.device, unconfig=unconfig,
                                             cli_config=configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
                # RouteAttributes
                class RouteAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False,
                                     **kwargs):
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # InterfaceAttributes
                        for sub, attributes2 in attributes.mapping_values('interface_attr',
                                                                          sort=True,
                                                                          keys=self.interface_attr):

                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))
                        # NextHopAttributes
                        for sub, attributes2 in attributes.mapping_values('next_hop_attr',
                                                                          sort=True,
                                                                          keys=self.next_hop_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                        if apply:
                            if configurations:
                                self.device.configure(configurations)
                        else:
                            return CliConfig(device=self.device, unconfig=unconfig,
                                             cli_config=configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                    class InterfaceAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False,
                                         **kwargs):
                            assert not apply
                            assert not kwargs, kwargs
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            if attributes.value('route'):
                               join_all = "{}".format(attributes.value('route'))

                            if attributes.value('interface'):
                                join_all += " {}".format(attributes.value('interface'))

                            if attributes.value('if_nexthop'):
                                join_all += ' {}'.format(attributes.value('if_nexthop'))

                            if attributes.value('if_preference'):
                                join_all += ' {}'.format(attributes.value('if_preference'))

                            if attributes.value('if_tag'):
                                join_all += " tag {}".format(attributes.value('if_tag'))

                            if attributes.value('if_track'):
                                join_all += " track {}".format(attributes.value('if_track'))

                            configurations.append_line(join_all)

                            if apply:
                                if configurations:
                                    self.device.configure(configurations)
                            else:
                                return CliConfig(device=self.device, unconfig=unconfig,
                                                 cli_config=configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

                    class NextHopAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False,
                                         **kwargs):
                            assert not apply
                            assert not kwargs, kwargs
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            if attributes.value('route'):
                                join_all = "{}".format(attributes.value('route'))

                            if attributes.value('nexthop'):
                                join_all += ' {}'.format(attributes.value('nexthop'))

                            if attributes.value('preference'):
                                join_all += ' {}'.format(attributes.value('preference'))

                            if attributes.value('tag'):
                                join_all += " tag {}".format(attributes.value('tag'))

                            if attributes.value('track'):
                                join_all += " track {}".format(attributes.value('track'))

                            configurations.append_line(join_all)

                            if apply:
                                if configurations:
                                    self.device.configure(configurations)
                            else:
                                return CliConfig(device=self.device, unconfig=unconfig,
                                                 cli_config=configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply,
                                                     attributes=attributes,
                                                     unconfig=True, **kwargs)

