# feature_cc_library.bzl
load("@bazel_skylib//rules:common_settings.bzl", "BuildSettingInfo")

def autoconf_cc_library(name, flags):
    print("Creating autoconf library header: " + name)
    all_flags_header_file(
      name = name + "_all",
      build_settings = flags,
      visibility = ["//visibility:public"],
    )

    native.cc_library(
        name = name,
        hdrs = [":" + name + "_all"],
        visibility = ["//visibility:public"],
    )

def _all_flags_header_file_impl(ctx):
    out = ctx.actions.declare_file(ctx.attr.header_name)
    content = "#pragma once\n"
    for flag in ctx.attr.build_settings:
        value = flag[BuildSettingInfo].value
        if type(value) == type(True):
            if value:
                value = 1
            else:
                # Don't define bool symbols set to false.
                continue
        content += "#define {} {}\n".format(
            flag.label.name.upper(),
            value
        )

    ctx.actions.write(
        output = out,
        content = content,
    )
    return [DefaultInfo(files = depset([out]))]

all_flags_header_file = rule(
    implementation = _all_flags_header_file_impl,
    attrs = {
        "header_name": attr.string(
            doc = "Name of the header to generate",
            default = "autoconf.h",
        ),
        "build_settings": attr.label_list(
            doc = "Build setting (flag) to construct the header from.",
            mandatory = True,
        ),
    },
)
