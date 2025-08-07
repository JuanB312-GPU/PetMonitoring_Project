# Test Configuration for PetCare Monitor Unit Tests

import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_all_tests():
    """
    Ejecutar todas las pruebas unitarias del proyecto
    """
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def run_backend_tests():
    """
    Ejecutar solo las pruebas del backend
    """
    loader = unittest.TestLoader()
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    suite = loader.discover(backend_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def run_frontend_tests():
    """
    Ejecutar solo las pruebas del frontend
    Nota: Las pruebas de JavaScript requieren un entorno de pruebas como Jest
    """
    print("Las pruebas de frontend requieren Jest o un framework similar.")
    print("Para ejecutar las pruebas de JavaScript:")
    print("1. Instalar Jest: npm install --save-dev jest")
    print("2. Configurar package.json con scripts de test")
    print("3. Ejecutar: npm test")
    
    return None

if __name__ == '__main__':
    print("=== Ejecutando todas las pruebas unitarias ===")
    result = run_all_tests()
    
    if result.wasSuccessful():
        print("\n✅ Todas las pruebas pasaron exitosamente!")
    else:
        print(f"\n❌ {len(result.failures)} pruebas fallaron")
        print(f"❌ {len(result.errors)} errores encontrados")
        
        # Mostrar detalles de las fallas
        if result.failures:
            print("\nFALLAS:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
                
        if result.errors:
            print("\nERRORES:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
