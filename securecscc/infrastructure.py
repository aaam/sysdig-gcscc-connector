from functools import lru_cache
import json

import sdcclient
import requests

import googleapiclient.discovery
from google.cloud import securitycenter
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2, struct_pb2


class GoogleCloudClient:
    _CREDENTIAL_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    def __init__(self, credentials):
        self._credentials = credentials

    def create_finding(self, organization, finding):
        source_finding = {
            'id': finding['id'],
            'category': finding['category'],
            'asset_ids': finding['asset_ids'],
            'source_id': finding['source_id'],
            'event_time': timestamp_pb2.Timestamp(seconds=finding['event_time']),
            'url': finding['url'],
            'properties': {
                'fields': {self._replace_dots(key): struct_pb2.Value(string_value=str(value)) for key, value in finding.get('properties', {}).items()}
            }
        }

        return self._security_client.create_finding(organization,
                                                    source_finding)

    def _replace_dots(self, value):
        return value.replace('.', '_')

    @property
    @lru_cache(maxsize=1)
    def _security_client(self):
        credentials = service_account.Credentials \
            .from_service_account_info(self._credentials.security_service_account_info())
        scoped_credentials = credentials.with_scopes(self._CREDENTIAL_SCOPES)

        return \
            securitycenter.SecurityCenterClient(credentials=scoped_credentials)

    def get_instance_id_from_hostname(self, project, zone, hostname):
        response = self._compute_engine_client.instances()\
            .list(project=project, zone=zone, fields="items(id,name)")\
            .execute()
        instances = {item['name']: item['id'] for item in response['items']}

        return instances.get(hostname)

    @property
    @lru_cache(maxsize=1)
    def _compute_engine_client(self):
        credentials = service_account.Credentials \
            .from_service_account_info(self._credentials.compute_service_account_info())

        return googleapiclient.discovery.build('compute',
                                               'v1',
                                               credentials=credentials)


class SysdigSecureClient:
    _MINUTE = 60
    _PAGING = {'from': 0, 'to': 200}

    def __init__(self, credentials):
        self._credentials = credentials
        self._policies = {}

    def events_happened_on_last_minute(self):
        result = self._sysdig_secure_client\
            .get_policy_events_duration(self._MINUTE)

        return result[1]['data']['policyEvents']

    @property
    @lru_cache(maxsize=1)
    def _sysdig_secure_client(self):
        return sdcclient.SdSecureClient(self._credentials.sysdig_token())

    def find_policy_by_id(self, policy_id):
        if self._policies == {}:
            policies = self._sysdig_secure_client.list_policies()
            for policy in policies[1]['policies']:
                self._policies[policy['id']] = policy['name']

        return self._policies[policy_id]

    def find_host_by_mac(self, mac):
        metrics = [{"id": "host.mac"}, {"id": "host.hostName"}]
        hosts = self._get_data_and_transform_to_dict(metrics)

        return hosts.get(mac)

    def _get_data_and_transform_to_dict(self, metrics):
        response = self._sysdig_secure_client.get_data(metrics,
                                                       -self._MINUTE,
                                                       paging=self._PAGING)

        return {raw['d'][0]: raw['d'][1] for raw in (response[1]['data'])}

    def find_container_image_from_container_id(self, container_id):
        metrics = [{"id": "container.id"}, {"id": "container.image"}]
        images = self._get_data_and_transform_to_dict(metrics)

        return images.get(container_id)

    def find_container_metadata_from_container_id(self, container_id):
        response = self._sysdig_secure_client.get_data(self._container_metadata_metrics(),
                                                       -self._MINUTE,
                                                       paging=self._PAGING)

        metadata = {
            raw['d'][0]: self._build_container_metadata_entry(raw['d'])
            for raw in response[1]['data']
        }

        return metadata.get(container_id)

    def _container_metadata_metrics(self):
        return [{"id": "container.id"},
                {"id": "container.name"},
                {"id": "container.image"},
                {"id": "kubernetes.pod.name"},
                {"id": "kubernetes.deployment.name"},
                {"id": "kubernetes.namespace.name"},
                {"id": "agent.tag.cluster"}]

    def _build_container_metadata_entry(self, data):
        return {
            'container.id': data[0],
            'container.name': data[1],
            'container.image': data[2],
            'kubernetes.pod.name': data[3],
            'kubernetes.deployment.name': data[4],
            'kubernetes.namespace.name': data[5],
            'agent.tag': data[6]
        }

    def create_webhook_notification_channel(self, channel_name, url, authentication_token):
        channel = self._find_notification_channel_by_name(channel_name)

        if channel is None:
            response = self._sysdig_secure_client.\
                create_webhook_notification_channel(channel_name, url)
            if response[0] == True:
                channel = response[1]['notificationChannel']

        channel['options']['additionalHeaders'] = {'Authorization': authentication_token}
        response = self._sysdig_secure_client.update_notification_channel(channel)
        if response[0] is True:
            return response[1]['notificationChannel']

        return None

    def _find_notification_channel_by_name(self, channel_name):
        response = self._sysdig_secure_client.get_notification_ids([{
            'type': 'WEBHOOK',
            'name': channel_name
        }])

        if response[0] is True:
            channel_id = response[1][0]
            response = self._sysdig_secure_client.get_notification_channel(channel_id)
            if response[0] is True:
                return response[1]

        return None

    def delete_notification_channel(self, channel_name):
        channel = self._find_notification_channel_by_name(channel_name)

        if channel is not None:
            self._sysdig_secure_client.delete_notification_channel(channel)


# FIXME: Please, avoid evil hacks and send a PR
def _create_webhook_notification_channel(sysdig_client, channel_name, url):
    channel_json = {
        'notificationChannel': {
            'type': 'WEBHOOK',
            'name': channel_name,
            'enabled': True,
            'options': {
                'notifyOnOk': False,
                'url': url,
                'notifyOnResolve': False,
            }
        }
    }

    res = requests.post(sysdig_client.url + '/api/notificationChannels',
                        headers=sysdig_client.hdrs,
                        data=json.dumps(channel_json),
                        verify=sysdig_client.ssl_verify)

    if not sysdig_client._checkResponse(res):
        return [False, sysdig_client.lasterr]
    return [True, res.json()]


sdcclient.SdSecureClient.create_webhook_notification_channel = \
    _create_webhook_notification_channel
