# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import google.cloud.securitycenter_v1alpha3.proto.messages_pb2 as google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2


class SecurityCenterStub(object):
  """Service for Cloud Security Command Center.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SearchAssets = channel.unary_unary(
        '/google.cloud.securitycenter.v1alpha3.SecurityCenter/SearchAssets',
        request_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchAssetsRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchAssetsResponse.FromString,
        )
    self.ModifyAsset = channel.unary_unary(
        '/google.cloud.securitycenter.v1alpha3.SecurityCenter/ModifyAsset',
        request_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.ModifyAssetRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Asset.FromString,
        )
    self.SearchFindings = channel.unary_unary(
        '/google.cloud.securitycenter.v1alpha3.SecurityCenter/SearchFindings',
        request_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchFindingsRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchFindingsResponse.FromString,
        )
    self.CreateFinding = channel.unary_unary(
        '/google.cloud.securitycenter.v1alpha3.SecurityCenter/CreateFinding',
        request_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.CreateFindingRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Finding.FromString,
        )
    self.ModifyFinding = channel.unary_unary(
        '/google.cloud.securitycenter.v1alpha3.SecurityCenter/ModifyFinding',
        request_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.ModifyFindingRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Finding.FromString,
        )


class SecurityCenterServicer(object):
  """Service for Cloud Security Command Center.
  """

  def SearchAssets(self, request, context):
    """Search assets within an organization.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ModifyAsset(self, request, context):
    """Modifies the marks on the specified asset.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchFindings(self, request, context):
    """Search findings within an organization.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateFinding(self, request, context):
    """Creates a finding, creating the same finding with a later event_time will
    update the existing one. CSCC provides the capability for users to search
    findings based on timestamps.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ModifyFinding(self, request, context):
    """Provides a way for users to update mutable parts of a given finding.
    Modifies marks on a finding.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SecurityCenterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SearchAssets': grpc.unary_unary_rpc_method_handler(
          servicer.SearchAssets,
          request_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchAssetsRequest.FromString,
          response_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchAssetsResponse.SerializeToString,
      ),
      'ModifyAsset': grpc.unary_unary_rpc_method_handler(
          servicer.ModifyAsset,
          request_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.ModifyAssetRequest.FromString,
          response_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Asset.SerializeToString,
      ),
      'SearchFindings': grpc.unary_unary_rpc_method_handler(
          servicer.SearchFindings,
          request_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchFindingsRequest.FromString,
          response_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.SearchFindingsResponse.SerializeToString,
      ),
      'CreateFinding': grpc.unary_unary_rpc_method_handler(
          servicer.CreateFinding,
          request_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.CreateFindingRequest.FromString,
          response_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Finding.SerializeToString,
      ),
      'ModifyFinding': grpc.unary_unary_rpc_method_handler(
          servicer.ModifyFinding,
          request_deserializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.ModifyFindingRequest.FromString,
          response_serializer=google_dot_cloud_dot_securitycenter__v1alpha3_dot_proto_dot_messages__pb2.Finding.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.cloud.securitycenter.v1alpha3.SecurityCenter', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
