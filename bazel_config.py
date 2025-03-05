import pathlib
import argparse
import kconfiglib
import sys


def write_kconfig_build_file(
    ostream,
    kconfig: kconfiglib.Kconfig,
) -> None:
    ostream.write(
        """load("@bazel_skylib//rules:common_settings.bzl",
    "bool_flag",
    "int_flag",
)
"""
    )
    for sym_name, sym in kconfig.syms.items():
        if sym is None or sym.type == kconfiglib.UNKNOWN:
            continue
        for sym_str in str(sym).splitlines():
            ostream.write(f"# {sym_str}\n")
        if sym.type == kconfiglib.INT:
            ostream.write(
                f"""int_flag(
    name = "CONFIG_{sym_name}",
    build_setting_default=0,
    visibility = ["//visibility:public"],
)
"""
            )
        if sym.type == kconfiglib.BOOL:
            ostream.write(
                f"""bool_flag(
    name = "CONFIG_{sym_name}",
    build_setting_default=False,
    visibility = ["//visibility:public"],
)
config_setting(
    name = "CONFIG_{sym_name}=true",
    flag_values = {{
        ":CONFIG_{sym_name}": "true",
    }},
)
"""
            )

    ostream.write('\nload(":feature_cc_library.bzl", "autoconf_cc_library")\n')
    ostream.write("autoconf_cc_library(\n")
    ostream.write('    name = "autoconf",\n')
    ostream.write("    flags = [\n")
    for sym_name, sym in kconfig.syms.items():
        if sym is None or sym.type == kconfiglib.UNKNOWN:
            continue
        ostream.write(f'        ":CONFIG_{sym_name}",\n')
    ostream.write("    ],\n")
    ostream.write(")\n")


def write_project_build_file(
    ostream,
    kconfig: kconfiglib.Kconfig,
) -> None:
    ostream.write("KCONFIG_FLAGS = [\n")
    for sym in kconfig.unique_defined_syms:
        if sym is None or sym.type == kconfiglib.UNKNOWN:
            continue

        name = f"@kconfig//:CONFIG_{sym.name}"
        if sym.type == kconfiglib.INT:
            value = sym.str_value
        elif sym.type == kconfiglib.BOOL:
            value = "true" if sym.str_value == 'y' else "false"
        else:
            raise RuntimeError(f"Unsupported symbol type: {sym.type}")
        ostream.write(f"        \"--{name}={value}\",\n")
    ostream.write("]\n")


def generate_kconfig_build_file(
    kconfig_path: pathlib.Path,
    out: pathlib.Path | None,
) -> None:
    print("Loading Kconfig file: " + str(kconfig_path))
    kconfig = kconfiglib.Kconfig(filename=kconfig_path)
    kconfig.load_allconfig(kconfig_path)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            write_kconfig_build_file(ostream=f, kconfig=kconfig)
    else:
        write_kconfig_build_file(ostream=sys.stdout, kconfig=kconfig)


def generate_project_build_file(
    kconfig_path: pathlib.Path,
    project_path: pathlib.Path,
    out: pathlib.Path | None,
) -> None:
    print("Loading Kconfig file: " + str(kconfig_path))
    kconfig = kconfiglib.Kconfig(filename=kconfig_path)
    kconfig.load_config(filename=project_path)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            write_project_build_file(ostream=f, kconfig=kconfig)
    else:
        write_project_build_file(ostream=sys.stdout, kconfig=kconfig)
    pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Kconfig bazel port")

    parser.add_argument(
        "--kconfig",
        type=pathlib.Path,
        help="Kconfig to load",
        required=True,
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
    )

    gen_kconfig_parser = subparsers.add_parser(
        "gen_kconfig",
        help="Generate generic kconfig BUILD",
    )
    gen_kconfig_parser.add_argument(
        "-o",
        type=pathlib.Path,
        help="Output file",
    )

    gen_project_parser = subparsers.add_parser(
        "gen_project",
        help="Generate BUILD file for a specific peroject",
    )
    gen_project_parser.add_argument(
        "--project",
        type=pathlib.Path,
        help="Project config file",
    )
    gen_project_parser.add_argument(
        "-o",
        type=pathlib.Path,
        help="Output file",
    )

    args = parser.parse_args()

    kconfig_path = args.kconfig
    subcommand = args.subcommand

    if subcommand == "gen_kconfig":
        generate_kconfig_build_file(
            kconfig_path=kconfig_path,
            out=args.o,
        )
    elif subcommand == "gen_project":
        generate_project_build_file(
            kconfig_path=kconfig_path,
            project_path=args.project,
            out=args.o,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
