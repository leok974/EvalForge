# Tools Basics

Implement ToolContract + ToolRegistry.

- ToolContract(name, input_keys, fn)
- ToolRegistry.register(tool)
- ToolRegistry.call(name, **kwargs)
  - validates name exists
  - validates kwargs keys match tool.input_keys exactly
