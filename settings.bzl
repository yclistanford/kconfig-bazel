load("@bazel_skylib//rules:common_settings.bzl", "int_flag")
# config INT_VALUE
# 	int "The integer value"
# 	help
# 	  Some int value that we'll print.
int_flag(
    name = "CONFIG_INT_VALUE",
)
bool_flag(
    name = "DEFINE_CONFIG_INT_VALUE"
)

config_settings(
  name = "prj1_conf",
  flag_values = {
    "CONFIG_INT_VALUE": 5
  }
)

config_settings(
  name = "prj2_conf",
  flag_values = {
    "CONFIG_INT_VALUE": 10
  }
)