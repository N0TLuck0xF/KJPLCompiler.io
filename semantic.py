class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Tracks variables and their types
        self.errors = []        # Collects semantic errors

    def analyze(self, syntax_tree):
        """
        Traverse the syntax tree and perform semantic checks.
        """
        self._check_statements(syntax_tree)
        return self.errors

    def _check_statements(self, node):
        """
        Check a block of statements (e.g., assignments, function calls).
        """
        for statement in node.statements:
            if statement.type == "assignment":
                self._check_assignment(statement)
            elif statement.type == "print":
                self._check_print(statement)
            # Add other statement types (e.g., loops, conditionals) here

    def _check_assignment(self, node):
        """
        Check variable assignments (e.g., x = 10 + "hello").
        """
        var_name = node.left.value
        var_type = self._infer_type(node.left)  # Type of left-hand side (LHS)
        expr_type = self._infer_type(node.right)  # Type of right-hand side (RHS)

        # Check if variable exists in symbol table
        if var_name not in self.symbol_table:
            self.symbol_table[var_name] = expr_type  # Implicit declaration (modify if KJPL requires explicit)
        else:
            # Ensure type consistency
            if self.symbol_table[var_name] != expr_type:
                self.errors.append(
                    f"Type mismatch: '{var_name}' is {self.symbol_table[var_name]}, but assigned {expr_type}."
                )

    def _check_print(self, node):
        """
        Check validity of print statements (e.g., print(undeclared_var)).
        """
        for arg in node.args:
            if arg.type == "identifier":
                if arg.value not in self.symbol_table:
                    self.errors.append(f"Undefined variable '{arg.value}' in print statement.")
            # Add type-checking logic if needed (e.g., print only accepts integers)

    def _infer_type(self, node):
        """
        Determine the type of an expression (e.g., 10 + "hello" is invalid).
        """
        if node.type == "number":
            return "int"
        elif node.type == "string":
            return "str"
        elif node.type == "identifier":
            if node.value in self.symbol_table:
                return self.symbol_table[node.value]
            else:
                self.errors.append(f"Undefined variable '{node.value}'.")
                return "unknown"
        elif node.type == "binary_op":
            left_type = self._infer_type(node.left)
            right_type = self._infer_type(node.right)
            if left_type != right_type:
                self.errors.append(
                    f"Type mismatch in operation: {left_type} vs {right_type}."
                )
                return "error"
            return left_type  # Assume valid if types match
        # Add more types (e.g., boolean, arrays) as needed
        return "unknown"
