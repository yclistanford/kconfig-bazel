load("@bazel_skylib//rules:common_settings.bzl",
    "bool_flag",
    "int_flag",
)
# config INT_VALUE
#       int "The integer value"
#       help
#         Some int value that we'll print.
int_flag(
    name = "CONFIG_INT_VALUE",
    build_setting_default=0,
    visibility = ["//visibility:public"],
)
# config FEATURE1
#       bool "Enable feature 1"
bool_flag(
    name = "CONFIG_FEATURE1",
    build_setting_default=False,
    visibility = ["//visibility:public"],
)
config_setting(
    name = "CONFIG_FEATURE1=true",
    flag_values = {
        ":CONFIG_FEATURE1": "true",
    },
)
# config FEATURE2
#       bool "Enable feature 2"
bool_flag(
    name = "CONFIG_FEATURE2",
    build_setting_default=False,
    visibility = ["//visibility:public"],
)
config_setting(
    name = "CONFIG_FEATURE2=true",
    flag_values = {
        ":CONFIG_FEATURE2": "true",
    },
)

load(":feature_cc_library.bzl", "autoconf_cc_library")
autoconf_cc_library(
    name = "autoconf",
    flags = [
        ":CONFIG_INT_VALUE",
        ":CONFIG_FEATURE1",
        ":CONFIG_FEATURE2",
    ],
)