# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ros/geometry_msgs/Transform.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ros.geometry_msgs import Quaternion_pb2 as ros_dot_geometry__msgs_dot_Quaternion__pb2
from ros.geometry_msgs import Vector3_pb2 as ros_dot_geometry__msgs_dot_Vector3__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!ros/geometry_msgs/Transform.proto\x12\x11ros.geometry_msgs\x1a\"ros/geometry_msgs/Quaternion.proto\x1a\x1fros/geometry_msgs/Vector3.proto\"m\n\tTransform\x12/\n\x0btranslation\x18\x01 \x01(\x0b\x32\x1a.ros.geometry_msgs.Vector3\x12/\n\x08rotation\x18\x02 \x01(\x0b\x32\x1d.ros.geometry_msgs.Quaternionb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ros.geometry_msgs.Transform_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRANSFORM._serialized_start=125
  _TRANSFORM._serialized_end=234
# @@protoc_insertion_point(module_scope)
