// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ex09_interface:msg/FullNameMessage.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ex09_interface/msg/detail/full_name_message__rosidl_typesupport_introspection_c.h"
#include "ex09_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ex09_interface/msg/detail/full_name_message__functions.h"
#include "ex09_interface/msg/detail/full_name_message__struct.h"


// Include directives for member types
// Member `last_name`
// Member `name`
// Member `first_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ex09_interface__msg__FullNameMessage__init(message_memory);
}

void ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_fini_function(void * message_memory)
{
  ex09_interface__msg__FullNameMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_member_array[3] = {
  {
    "last_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ex09_interface__msg__FullNameMessage, last_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ex09_interface__msg__FullNameMessage, name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "first_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ex09_interface__msg__FullNameMessage, first_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_members = {
  "ex09_interface__msg",  // message namespace
  "FullNameMessage",  // message name
  3,  // number of fields
  sizeof(ex09_interface__msg__FullNameMessage),
  ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_member_array,  // message members
  ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_type_support_handle = {
  0,
  &ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ex09_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ex09_interface, msg, FullNameMessage)() {
  if (!ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_type_support_handle.typesupport_identifier) {
    ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ex09_interface__msg__FullNameMessage__rosidl_typesupport_introspection_c__FullNameMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
