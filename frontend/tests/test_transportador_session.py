"""
Testes de Selenium para validar a persistência de sessão e acesso às funcionalidades do Transportador.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

BASE_URL = "https://xbpneus-frontend.onrender.com"
TRANSPORTADOR_EMAIL = "transportador.teste2@xbpneus.com"
TRANSPORTADOR_PASSWORD = "Teste@2025"


@pytest.fixture
def driver():
    """Fixture para criar e fechar o driver do Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    driver.quit()


class TestTransportadorSession:
    """Testes para validar a persistência de sessão do Transportador."""
    
    def test_login_success(self, driver):
        """Testa se o login é bem-sucedido."""
        driver.get(f"{BASE_URL}/")
        
        # Preencher email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(TRANSPORTADOR_EMAIL)
        
        # Preencher senha
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TRANSPORTADOR_PASSWORD)
        
        # Clicar no botão Entrar
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        # Aguardar redirecionamento para o dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Relatórios')]"))
        )
        
        # Verificar se estamos no dashboard
        assert "/dashboard" in driver.current_url
        print(f"✓ Login bem-sucedido. URL atual: {driver.current_url}")
    
    def test_access_relatorios_after_login(self, driver):
        """Testa se conseguimos acessar a página de Relatórios após o login."""
        # Fazer login
        driver.get(f"{BASE_URL}/")
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(TRANSPORTADOR_EMAIL)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TRANSPORTADOR_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        # Aguardar redirecionamento para o dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Relatórios')]"))
        )
        
        # Clicar em Relatórios
        relatorios_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Relatórios')]")
        relatorios_link.click()
        
        # Aguardar a página de Relatórios carregar
        time.sleep(2)
        
        # Verificar se estamos na página de Relatórios
        current_url = driver.current_url
        print(f"URL após clicar em Relatórios: {current_url}")
        
        # Verificar se o token ainda está no localStorage
        token = driver.execute_script("return localStorage.getItem('access_token');")
        user_role = driver.execute_script("return localStorage.getItem('user_role');")
        
        print(f"Token presente: {bool(token)}")
        print(f"User Role: {user_role}")
        
        # Verificar se não fomos redirecionados para o login
        assert "/login" not in current_url, f"Fomos redirecionados para o login. URL: {current_url}"
        assert "/relatorios" in current_url, f"Não estamos na página de Relatórios. URL: {current_url}"
        assert token, "Token não está no localStorage"
        assert user_role == "transportador", f"User Role incorreto: {user_role}"
        
        print("✓ Acesso a Relatórios bem-sucedido com sessão persistida")
    
    def test_access_frota_after_login(self, driver):
        """Testa se conseguimos acessar a página de Frota após o login."""
        # Fazer login
        driver.get(f"{BASE_URL}/")
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(TRANSPORTADOR_EMAIL)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TRANSPORTADOR_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        # Aguardar redirecionamento para o dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Frota')]"))
        )
        
        # Clicar em Frota
        frota_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Frota')]")
        frota_link.click()
        
        # Aguardar a página de Frota carregar
        time.sleep(2)
        
        # Verificar se estamos na página de Frota
        current_url = driver.current_url
        print(f"URL após clicar em Frota: {current_url}")
        
        # Verificar se não fomos redirecionados para o login
        assert "/login" not in current_url, f"Fomos redirecionados para o login. URL: {current_url}"
        assert "/frota" in current_url, f"Não estamos na página de Frota. URL: {current_url}"
        
        print("✓ Acesso a Frota bem-sucedido com sessão persistida")
    
    def test_access_pneus_after_login(self, driver):
        """Testa se conseguimos acessar a página de Pneus após o login."""
        # Fazer login
        driver.get(f"{BASE_URL}/")
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(TRANSPORTADOR_EMAIL)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TRANSPORTADOR_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        # Aguardar redirecionamento para o dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pneus')]"))
        )
        
        # Clicar em Pneus
        pneus_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Pneus')]")
        pneus_link.click()
        
        # Aguardar a página de Pneus carregar
        time.sleep(2)
        
        # Verificar se estamos na página de Pneus
        current_url = driver.current_url
        print(f"URL após clicar em Pneus: {current_url}")
        
        # Verificar se não fomos redirecionados para o login
        assert "/login" not in current_url, f"Fomos redirecionados para o login. URL: {current_url}"
        assert "/pneus" in current_url, f"Não estamos na página de Pneus. URL: {current_url}"
        
        print("✓ Acesso a Pneus bem-sucedido com sessão persistida")
    
    def test_console_logs_on_relatorios_access(self, driver):
        """Testa se os logs de depuração aparecem no console ao acessar Relatórios."""
        # Fazer login
        driver.get(f"{BASE_URL}/")
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(TRANSPORTADOR_EMAIL)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TRANSPORTADOR_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        # Aguardar redirecionamento para o dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Relatórios')]"))
        )
        
        # Limpar logs anteriores
        driver.execute_script("console.clear();")
        
        # Clicar em Relatórios
        relatorios_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Relatórios')]")
        relatorios_link.click()
        
        # Aguardar a página de Relatórios carregar
        time.sleep(2)
        
        # Obter logs do console
        logs = driver.get_log('browser')
        console_messages = [log['message'] for log in logs if 'ProtectedRoute' in log['message']]
        
        print(f"Console logs encontrados: {console_messages}")
        
        # Verificar se os logs de depuração aparecem
        assert len(console_messages) > 0, "Nenhum log de depuração encontrado no console"
        
        print("✓ Logs de depuração encontrados no console")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

