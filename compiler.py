import logging
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

# --------------------------
# Logger Setup
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("compiler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --------------------------
# Compiler Class
# --------------------------
class KJPLCompiler:
    def __init__(self):
        self.lexer = lexer
        self.parser = parser
        self.semantic_analyzer = SemanticAnalyzer()
        self.code_generator = CodeGenerator()

    def compile(self, source_code):
        """
        Compile KJPL source code into C code.
        """
        try:
            logger.info("Starting compilation process...")

            # Step 1: Lexical Analysis
            logger.info("Running lexical analysis...")
            tokens = self._lexical_analysis(source_code)
            logger.info("Lexical analysis completed successfully.")

            # Step 2: Syntax Analysis
            logger.info("Running syntax analysis...")
            ast = self._syntax_analysis(tokens)
            logger.info("Syntax analysis completed successfully.")

            # Step 3: Semantic Analysis
            logger.info("Running semantic analysis...")
            self._semantic_analysis(ast)
            logger.info("Semantic analysis completed successfully.")

            # Step 4: Code Generation
            logger.info("Generating target code...")
            c_code = self._code_generation(ast)
            logger.info("Code generation completed successfully.")

            logger.info("Compilation process completed successfully.")
            return c_code

        except Exception as e:
            logger.error(f"Compilation failed: {e}")
            raise

    def _lexical_analysis(self, source_code):
        """
        Tokenize the source code.
        """
        self.lexer.input(source_code)
        tokens = list(self.lexer)
        if not tokens:
            raise ValueError("No tokens generated. Source code may be empty or invalid.")
        return tokens

    def _syntax_analysis(self, tokens):
        """
        Parse tokens into an Abstract Syntax Tree (AST).
        """
        ast = self.parser.parse(source_code)
        if not ast:
            raise SyntaxError("Failed to generate AST. Invalid syntax.")
        return ast

    def _semantic_analysis(self, ast):
        """
        Perform semantic checks on the AST.
        """
        errors = self.semantic_analyzer.analyze(ast)
        if errors:
            error_msg = "\n".join(errors)
            raise ValueError(f"Semantic errors found:\n{error_msg}")

    def _code_generation(self, ast):
        """
        Generate C code from the AST.
        """
        c_code = self.code_generator.generate(ast)
        if not c_code:
            raise ValueError("Failed to generate target code.")
        return c_code

# --------------------------
# Main Function
# --------------------------
def main():
    # Sample KJPL source code
    source_code = """
    let x = 10;
    fn add(a: int, b: int) -> int {
        return a + b;
    }
    print(add(x, 5));
    """

    # Initialize and run the compiler
    compiler = KJPLCompiler()
    try:
        c_code = compiler.compile(source_code)
        print("Generated C Code:\n")
        print(c_code)
    except Exception as e:
        logger.error(f"Compilation failed: {e}")

if __name__ == "__main__":
    main()
