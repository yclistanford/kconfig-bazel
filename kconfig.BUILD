load("@bazel_skylib//rules:common_settings.bzl",
    "bool_flag",
    "int_flag",
)

bool_flag(
    name = "CONFIG_FEATURE1",
    build_setting_default=False,    
    visibility = ["//visibility:public"],
)
bool_flag(
    name = "CONFIG_FEATURE2",
    build_setting_default=False,
    visibility = ["//visibility:public"],
)
int_flag(
    name = "CONFIG_INT_VALUE",
    build_setting_default=0,
    visibility = ["//visibility:public"],
)

config_setting(
  name = "CONFIG_FEATURE1=true",
  flag_values = {
    ":CONFIG_FEATURE1": "true",
  },
)
config_setting(
  name = "CONFIG_FEATURE2=true",
  flag_values = {
    ":CONFIG_FEATURE2": "true",
  },
)