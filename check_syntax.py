import py_compile
import sys

def check_file(filepath):
    try:
        py_compile.compile(filepath, doraise=True)
        print(f"{filepath} is OK")
    except py_compile.PyCompileError as e:
        print(f"Error in {filepath}:\n{e}")
        with open('compile_errors.txt', 'a') as f:
            f.write(f"Error in {filepath}:\n{e}\n")

check_file(r'e:\AgaShop\github-cpanel-agashop\backend\api\shops\viewsets\ProductViewSet.py')
check_file(r'e:\AgaShop\github-cpanel-agashop\backend\api\shops\viewsets\SupplyViewSet.py')
