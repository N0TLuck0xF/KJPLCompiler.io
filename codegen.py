# codegen.py
class CodeGenerator:
    def __init__(self):
        self.output = []
        self.indent_level = 0
        self.current_function = None
        self.symbol_table = {}  # Track variables and their types
        self.label_counter = 0   # For generating unique labels

    # --------------------------
    # Main Generation Entry Point
    # --------------------------
    def generate(self, ast_node):
        self.visit(ast_node)
        return "\n".join(self.output)

    # --------------------------
    # Visitor Pattern Dispatcher
    # --------------------------
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {type(node).__name__}")

    # --------------------------
    # AST Node Handlers
    # --------------------------
    def visit_ProgramNode(self, node):
        self._add_line("#include <stdio.h>")
        self._add_line("#include <stdlib.h>\n")
        
        # Generate forward declarations first
        for stmt in node.statements:
            if isinstance(stmt, ast_nodes.FunctionNode):
                self._add_line(f"int {stmt.name}({self._gen_params(stmt.params)});")
        
        self._add_line("\n// Main Program")
        self._add_line("int main() {")
        self.indent_level += 1
        
        for stmt in node.statements:
            if not isinstance(stmt, ast_nodes.FunctionNode):
                self.visit(stmt)
        
        self.indent_level -= 1
        self._add_line("return 0;")
        self._add_line("}\n")
        
        # Generate functions
        for stmt in node.statements:
            if isinstance(stmt, ast_nodes.FunctionNode):
                self.visit(stmt)

    def visit_FunctionNode(self, node):
        self.current_function = node.name
        params = ", ".join([f"int {param}" for param in node.params])
        
        self._add_line(f"\nint {node.name}({params}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        if node.return_expression:
            ret_val = self.visit(node.return_expression)
            self._add_line(f"return {ret_val};")
        else:
            self._add_line("return 0;")
        
        self.indent_level -= 1
        self._add_line("}")
        self.current_function = None

    def visit_AssignmentNode(self, node):
        var_name = node.identifier.name
        expr_value = self.visit(node.expression)
        
        # Track variable types (simplified - assumes int unless specified)
        if var_name not in self.symbol_table:
            self.symbol_table[var_name] = 'int'
            self._add_line(f"int {var_name} = {expr_value};")
        else:
            self._add_line(f"{var_name} = {expr_value};")

    def visit_PrintNode(self, node):
        expr_value = self.visit(node.expression)
        self._add_line(f'printf("%d\\n", {expr_value});')

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        self._add_line(f"if ({condition}) {{")
        self.indent_level += 1
        
        for stmt in node.then_block:
            self.visit(stmt)
        
        self.indent_level -= 1
        if node.else_block:
            self._add_line("} else {")
            self.indent_level += 1
            for stmt in node.else_block:
                self.visit(stmt)
            self.indent_level -= 1
        self._add_line("}")

    def visit_WhileNode(self, node):
        condition = self.visit(node.condition)
        loop_start = self._new_label()
        loop_end = self._new_label()
        
        self._add_line(f"{loop_start}:")
        self._add_line(f"if (!({condition})) goto {loop_end};")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self._add_line(f"goto {loop_start};")
        self.indent_level -= 1
        self._add_line(f"{loop_end}:")

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.operator} {right})"

    def visit_NumberNode(self, node):
        return str(node.value)

    def visit_IdentifierNode(self, node):
        if node.name not in self.symbol_table:
            raise CodegenError(f"Undefined variable '{node.name}'")
        return node.name

    def visit_ConditionNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.operator} {right})"

    # --------------------------
    # Helper Methods
    # --------------------------
    def _add_line(self, text):
        self.output.append("    " * self.indent_level + text)

    def _new_label(self):
        self.label_counter += 1
        return f"label_{self.label_counter}"

    def _gen_params(self, params):
        return ", ".join([f"int {p}" for p in params])

# --------------------------
# Custom Exceptions
# --------------------------
class CodegenError(Exception):
    pass

# --------------------------
# Usage Example
# --------------------------
if __name__ == "__main__":
    # Sample AST for testing
    from parser import ast_nodes

    ast = ast_nodes.ProgramNode(statements=[
        ast_nodes.FunctionNode(
            name="add",
            params=["a", "b"],
            body=[
                ast_nodes.ReturnNode(
                    expression=ast_nodes.BinaryOpNode(
                        left=ast_nodes.IdentifierNode("a"),
                        operator="+",
                        right=ast_nodes.IdentifierNode("b")
                    )
                )
            ]
        ),
        ast_nodes.AssignmentNode(
            identifier=ast_nodes.IdentifierNode("x"),
            expression=ast_nodes.BinaryOpNode(
                left=ast_nodes.NumberNode(5),
                operator="+",
                right=ast_nodes.NumberNode(3)
            )
        ),
        ast_nodes.PrintNode(
            expression=ast_nodes.IdentifierNode("x")
        )
    ])

    generator = CodeGenerator()
    try:
        c_code = generator.generate(ast)
        print("Generated C Code:\n")
        print(c_code)
    except CodegenError as e:
        print(f"Code Generation Error: {e}")
