"""
Check Blueprint compile functions in unreal module
"""
import unreal

compile_funcs = [attr for attr in dir(unreal) if 'compile' in attr.lower() or 'blueprint' in attr.lower()]
unreal.log_warning(f"Blueprint/Compile related attrs: {compile_funcs}")
