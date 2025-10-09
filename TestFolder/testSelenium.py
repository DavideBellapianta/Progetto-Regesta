import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class FullUserJourneyTest(unittest.TestCase):

    def setUp(self):
        """Prepara il browser prima del test."""
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.base_url = "http://localhost:5173"
        self.driver.get(self.base_url)
        self.driver.maximize_window()

    def tearDown(self):
        """Pulisce e chiude il browser dopo il test."""
        print("Test completato. Il browser si chiuderà tra 5 secondi.")
        time.sleep(5)
        self.driver.quit()

    def test_full_user_journey(self):
        """Esegue l'intero percorso: login, ricerca, interazione, carrello e pagamento."""
        driver = self.driver
        wait = WebDriverWait(driver, 15)

        print("Step 1: Inizio procedura di login...")
        user_menu_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Apri menù utente']")))
        ActionChains(driver).move_to_element(user_menu_button).click().perform()
        login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Accedi")))
        login_link.click()
        email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        email_input.send_keys("test4@gmail.com")
        driver.find_element(By.ID, "password").send_keys("test423284aj")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Offerte del Giorno')]")))
        print("Login effettuato con successo.")

        print("Step 2-3: Ricerca e navigazione prodotto...")
        search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Cerca prodotti...']")))
        search_bar.send_keys("cioccolato")
        search_bar.send_keys(Keys.RETURN)
        product_card_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='tavoletta-di-cioccolato-fondente-85']")))
        driver.execute_script("arguments[0].click();", product_card_link)
        wait.until(EC.url_contains("/prodotto/tavoletta-di-cioccolato-fondente-85"))
        print("Navigazione alla pagina prodotto avvenuta.")
        
        print("Step 4: Interazione con la pagina di dettaglio...")
        add_to_cart_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Aggiungi al carrello')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
        time.sleep(1)
        add_to_cart_button.click()
        print("Prodotto aggiunto al carrello.")
        
        try:
            favorite_selectors = [
                "button[aria-label='Aggiungi ai preferiti']",
                "button[aria-label*='preferiti']",
                "button[title*='Preferiti']",
                "button[class*='favorite']",
                ".favorite-button",
                "button svg[aria-label*='preferiti']",
                "//button[contains(@class, 'favorite')]",
                "//button[.//svg[contains(@aria-label, 'preferiti')]]"
            ]
            
            favorite_button = None
            for selector in favorite_selectors:
                try:
                    if selector.startswith("//"):
                        favorite_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        favorite_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if favorite_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", favorite_button)
                time.sleep(1)
                favorite_button.click()
                print("Prodotto aggiunto ai preferiti.")
            else:
                print("Pulsante preferiti non trovato, procedo senza aggiungere ai preferiti")
                
        except Exception as e:
            print(f"Errore nell'aggiunta ai preferiti: {e}. Procedo comunque.")
        
        print("Step 5: Navigazione carrello e checkout...")
        cart_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Carrello']")))
        ActionChains(driver).move_to_element(cart_icon).click().perform()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Vai al Carrello"))).click()
        wait.until(EC.url_contains("/carrello"))
        print("Navigato alla pagina del carrello.")
        
        increase_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='+'])[1]")))
        increase_button.click()
        time.sleep(1) 
        decrease_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='-'])[1]")))
        decrease_button.click()
        print("Quantità modificata nel carrello.")

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Procedi al Checkout"))).click()
        wait.until(EC.url_contains("/pagamento"))
        print("Navigato alla pagina di pagamento.")

        print("Step 6: Compilazione dati...")
        wait.until(EC.visibility_of_element_located((By.ID, "telefono"))).send_keys("1234567890")
        driver.find_element(By.ID, "indirizzo").send_keys("Via Roma 1")
        driver.find_element(By.ID, "citta").send_keys("Brescia")
        driver.find_element(By.ID, "cap").send_keys("25121")
        driver.find_element(By.ID, "numeroCarta").send_keys("5030333443443443")
        driver.find_element(By.ID, "scadenzaCarta").send_keys("02/29")
        driver.find_element(By.ID, "cvc").send_keys("987")
        print("Dati inseriti.")
        
        pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Paga Ora')]")))
        ActionChains(driver).move_to_element(pay_button).click().perform()
        print("Bottone 'Paga Ora' cliccato.")
        
        wait.until(EC.url_contains("/profilo"))
        print("Pagamento simulato, reindirizzato correttamente al profilo.")

        print("Step 8: Verifica cronologia ordini e scontrino...")
        driver.execute_script("window.scrollBy(0, 300);")
        
        receipt_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(), 'Vedi Scontrino')])[1]")))
        main_window_handle = driver.current_window_handle
        receipt_button.click()
        print("Richiesto lo scontrino...")
        
        wait.until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != main_window_handle:
                driver.switch_to.window(window_handle)
                break
        
        wait.until(EC.title_contains("Scontrino Ordine"))
        self.assertIn("Scontrino Ordine", driver.title)
        print("Verifica finale superata: Lo scontrino è stato aperto in una nuova scheda.")


if __name__ == "__main__":
    unittest.main()