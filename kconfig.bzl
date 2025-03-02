def _gen_kconfiglib_impl(repo_ctx):
  repo_ctx.symlink(
    repo_ctx.attr.kconfig_file,
    "BUILD.bazel",
  )

gen_kconfiglib = repository_rule(
  implementation = _gen_kconfiglib_impl,
  attrs = {
    "kconfig_file": attr.label(
      allow_single_file=True,
      default="//:kconfig.BUILD",
    )
  }
)

def _libkconfig_impl(module_ctx):
  gen_kconfiglib(name="kconfig")

libkconfig = module_extension(
  doc = "",
  implementation = _libkconfig_impl,
)