# feature_cc_library.bzl
load("@bazel_skylib//rules:common_settings.bzl", "BuildSettingInfo")

def feature_cc_library(name, flag):
    hdrs_name = name + ".hdr"

    flag_header_file(
        name = hdrs_name,
        build_setting = flag,
    )

    native.cc_import(
        name = name,
        hdrs = [":" + hdrs_name],
    )

def autoconf_cc_library(name, flags):
    feature_libraries = []
    header_names = []
    for flag in flags:
        flag_label = Label(flag)
        lib_name = flag_label.name.lower() + "_cc"
        feature_libraries.append(lib_name)
        header_names.append(flag_label.name + ".h")
        feature_cc_library(
            name = lib_name,
            flag = flag,
        )

    print("Creating autoconf library header: " + name)
    all_flags_header_file(
      name = name + "_all",
      build_settings = flags,
    )

    native.cc_library(
        name = name,
        hdrs = [":" + name + "_all"],
        deps = [":" + feature_lib for feature_lib in feature_libraries],
        visibility = ["//visibility:public"],
    )


def _impl(ctx):
    out = ctx.actions.declare_file(ctx.attr.build_setting.label.name + ".h")

    # Convert boolean flags to canonical integer values.
    value = ctx.attr.build_setting[BuildSettingInfo].value
    if type(value) == type(True):
        if value:
            value = 1
        else:
            value = 0

    ctx.actions.write(
        output = out,
        content = r"""
#pragma once
#define {} {}
""".format(ctx.attr.build_setting.label.name.upper(), value),
    )
    return [DefaultInfo(files = depset([out]))]

flag_header_file = rule(
    implementation = _impl,
    attrs = {
        "build_setting": attr.label(
            doc = "Build setting (flag) to construct the header from.",
            mandatory = True,
        ),
    },
)

def _all_flags_header_file_impl(ctx):
    out = ctx.actions.declare_file(ctx.attr.header_name)
    content = "#pragma once\n"
    for flag in ctx.attr.build_settings:
        content += "#include \"{}.h\"\n".format(
            flag.label.name,
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
