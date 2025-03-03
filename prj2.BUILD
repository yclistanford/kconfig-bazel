load(":feature_cc_library.bzl", "autoconf_cc_library")

autoconf_cc_library(
    name = "autoconf",
    flags = [
        "@kconfig//:CONFIG_INT_VALUE",
        "@kconfig//:CONFIG_FEATURE1",
        "@kconfig//:CONFIG_FEATURE2",
    ],
)

platform(
    name = "platform",
    parents = ["@platforms//host"],
    flags = [
      "--@kconfig//:CONFIG_FEATURE1=true",
      "--@kconfig//:CONFIG_INT_VALUE=15",
    ],
    visibility = ["//visibility:public"],
)