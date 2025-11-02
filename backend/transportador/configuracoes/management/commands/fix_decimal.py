import sys
with open('importar_catalogos.py', 'r') as f:
    content = f.read()

# Substituir a função get_decimal
old_func = """                def get_decimal(value):
                    if not value or value.strip() == '':
                        return None
                    return float(value.replace(',', '.'))"""

new_func = """                def get_decimal(value):
                    if not value or value.strip() == '':
                        return None
                    # Remover ~ de valores aproximados
                    value = value.strip().replace('~', '').replace(',', '.')
                    return float(value)"""

content = content.replace(old_func, new_func)

with open('importar_catalogos.py', 'w') as f:
    f.write(content)

print("Função get_decimal corrigida")
