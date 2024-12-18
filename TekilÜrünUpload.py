import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox,QFileDialog, QListWidget
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import string

class SeleniumAutomationGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI components
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Selenium Automation GUI')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Username input field
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Enter Username')
        layout.addWidget(self.username_input)

        # Password input field
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.profile_input = QComboBox(self)
        self.profile_input.addItem("Profile 1")
        self.profile_input.addItem("Profile 5")
        layout.addWidget(self.profile_input)

        # Merchant SKU input field
        self.merchant_sku_input = QLineEdit(self)
        self.merchant_sku_input.setPlaceholderText('Enter Merchant SKU (comma separated)')
        layout.addWidget(self.merchant_sku_input)

        # Category selection dropdown
        self.category_input = QComboBox(self)
        self.category_input.addItem("Elbise")
        self.category_input.addItem("String")
        layout.addWidget(self.category_input)

        # Model code input field
        self.model_kodu_input = QLineEdit(self)
        self.model_kodu_input.setPlaceholderText('Enter Model Kodu')
        layout.addWidget(self.model_kodu_input)

        # Brand input field
        self.brand_input = QLineEdit(self)
        self.brand_input.setPlaceholderText('Enter Brand')
        layout.addWidget(self.brand_input)

        # Profit margin input field
        self.Kar_marjı_input = QLineEdit(self)
        self.Kar_marjı_input.setPlaceholderText('Enter Profit Margin')
        layout.addWidget(self.Kar_marjı_input)

        self.old_new_input = QLineEdit(self)
        self.old_new_input.setPlaceholderText('Enter Old:new (e.g. YNT:Velours Violet)')
        layout.addWidget(self.old_new_input)

        # Button to select images
        self.images_input = QPushButton("Select Images", self)
        self.images_input.clicked.connect(self.select_images)
        layout.addWidget(self.images_input)

        # List to display selected groups of images
        self.image_groups_list = QListWidget(self)
        layout.addWidget(self.image_groups_list)

        # Submit Button to start the automation process
        self.submit_button = QPushButton('Start Automation', self)
        self.submit_button.clicked.connect(self.start_automation)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Store selected image paths in separate groups
        self.image_groups = []

    def select_images(self):
        # Open file dialog to select images
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if files:
            # Store selected files as a new group
            self.image_groups.append(files)

            # Update the display list with the group of selected images
            self.image_groups_list.addItem(f"Group {len(self.image_groups)}: {len(files)} images")

    def start_automation(self):
        # Get user input from the fields
        username = self.username_input.text()
        password = self.password_input.text()
        merchant_sku = self.merchant_sku_input.text().split(',')
        Category = self.category_input.currentText()
        ModelKodu = self.model_kodu_input.text()
        Brand = self.brand_input.text()
        Kar_marjı = float(self.Kar_marjı_input.text())
        images = self.image_groups
        profile = self.profile_input.currentText()
        print(images)
        # Loop through each group of selected images and process them
        for group_index, group in enumerate(self.image_groups):
            print(f"Processing Group {group_index + 1}:")
            for file_path in group:
                print(f"Uploading {file_path}")
                

                # You can add the image upload logic here, passing file_path to your function
                # Get the old:new mapping input
        old_new_mapping = self.old_new_input.text()
        mappings = self.parse_old_new_mappings(old_new_mapping)


        # Initialize Selenium WebDriver
        self.run_selenium_automation(username, password, merchant_sku, Category, ModelKodu, Brand, Kar_marjı,images, mappings, profile)

    def parse_old_new_mappings(self, old_new_mapping):
    # Split the mappings by commas or line breaks
        mappings = []
        for mapping in old_new_mapping.split(','):
            old_new_pair = mapping.split(':')
            if len(old_new_pair) == 2:
                mappings.append((old_new_pair[0].strip(), old_new_pair[1].strip()))
        return mappings


    def run_selenium_automation(self, username, password, merchant_sku, Category, ModelKodu, Brand, Kar_marjı,images, mappings, profile):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_extension('C:/Users/ahmet/Desktop/Yazılım/VSCode_Projects/Datascrap for Trendyol API/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_59_0_0.crx') #ublock origin extension
        profile_path = fr"C:\Users\ahmet\AppData\Local\Google\Chrome\User Data\{profile}"
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Set up the Chrome driver
        service = Service(executable_path='C:/Users/ahmet/Desktop/Yazılım/chromedriver-win64/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Open the login page
        driver.get('https://partner.trendyol.com/account/login')

        # Wait until the dashboard is loaded or timeout
        try:
            WebDriverWait(driver, 2).until(EC.url_contains('dashboard'))
        except Exception:
            print("Dashboard did not load within the expected time.")


        time.sleep(5)

        # Open a new tab for the second login
        driver.execute_script("window.open('');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.get('https://www.yeninesiltoptanci.com/UyeGiris')



        try:
            driver.find_element(By.NAME, "txtUyeGirisEmail").send_keys(username)
            driver.find_element(By.NAME, "txtUyeGirisPassword").send_keys(password)
            driver.find_element(By.CLASS_NAME, "uyeGirisFormDetailButtonList").click()
        except Exception as e:
            print(f"Error during login: {e}")

        time.sleep(10)
        color_count = 1
        shippingFee = 61.9
        hizmetbedeli = 8.39
        commissionRate = 0.215
        # Search and interact with merchant SKU input
        for index,sku in enumerate(merchant_sku):
            try:
                merchant_sku_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "txtbxArama"))
                )
                # Clear any previous input and enter the new merchant SKU
                merchant_sku_input.clear()
                merchant_sku_input.send_keys(sku)
                # Wait for the search button to be clickable and click it
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnKelimeAra"))
                )
                search_button.click()

                product_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "productName.detailUrl"))
                )
                product_link.click()
            except Exception as e:
                print(f"Error interacting with merchant SKU elements: {e}")

            # Extract productDetailModel from page source
            page_source = driver.page_source
            match = re.search(r'var productDetailModel = ({.*?});', page_source, re.DOTALL)
            if match:
                product_detail_model = json.loads(match.group(1))
                products = product_detail_model.get('products', []) #Gets the details of the product
                print(products)

                original_product_name = product_detail_model.get('productName', '')
                print(f"Original Product Name: {original_product_name}")
                # Replace old with new in the product name
                updated_product_name = original_product_name
                for old, new in mappings:
                    updated_product_name = updated_product_name.replace(old, new)
                    print(f"Updated Product Name after replacing {old} with {new}: {updated_product_name}")


                tedarikci_values = [(item['tedarikciKodu'].split('|'),item.get("stokKodu"),item.get("stokAdedi"),item.get("urunFiyatiOrjinal"),item.get("urunFiyatiOrjinalKDV")) for item in products]
                print(tedarikci_values)
                color = tedarikci_values[0][0][2] 
                if color == "MAVİ" or color == "SİYAH":
                    color_mapping = { #Türkçe İngilizcedeki büyük İ farkından dolayı else teki block doğru çalışmıyor ve küçük sku olsa bile olmuyor
                    "MAVİ": "Mavi",
                    "SİYAH": "Siyah",
                    "YEŞİL": "Yeşil",
                    "LACİVERT": "Mavi",}
                    color = color_mapping.get(color, color.lower())
                else:
                    color = color[0].upper() + color[1:].casefold()


                if color == "Saks":
                    color = "Mavi"
                elif color == "Lila":
                    color = "Mor"
                elif color == "Fuşya" or color == "Pudra":
                    color = "Pembe"
                elif color == "Kirik beyaz":
                    color = "Beyaz"
                elif color == "Kirmizi":
                    color = "Kırmızı"


                fiyat = tedarikci_values[0][3]+tedarikci_values[0][4]
                satis_fiyati = (fiyat + shippingFee + hizmetbedeli)*(1+Kar_marjı)/(1-commissionRate)
                whole_part = int(satis_fiyati)
                decimal_part = ",90"
                formatted_price = f"{whole_part}{decimal_part}"
                print(f"Color: {color}")
                print(f"Fiyat: {fiyat}",f"Satis Fiyati: {satis_fiyati}")

                size_list = []
                stok_kodu_list = []
                stok_adedi_list = []
                for sku in tedarikci_values:
                    size_list.append(sku[0][3])
                    stok_kodu_list.append(sku[1])
                    stok_adedi_list.append(sku[2])
                print(f"Size List: {size_list}",f"Stok Kodu List: {stok_kodu_list}",f"Stok Adedi List: {stok_adedi_list}")


            else:
                print("Could not find the productDetailModel variable in the HTML.")

            # Switch back to the first tab and interact with Trendyol product page
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://partner.trendyol.com/products/single-product")
            driver.execute_script("document.body.style.zoom='50%'")
            try:
                trendyol_product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Ürün adı giriniz"]')) #Trendyola ürün ismini giriyor
                )
                trendyol_product_name.send_keys(updated_product_name)

                reset_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Ürün Bilgileri")]')) #Ürün bilgilerine tıklayıp dropdownu kapatıyor
                )
                reset_button.click()

                # Select category
                time.sleep(5)
                category_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "input-container")) #Kategori kutusuna tıklayıp dropdownu açıyor
                )
                category_box.click()

                category_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#select-category .form-control")) 
                )
                category_input.clear()
                category_input.send_keys(Category) #Kategori ismini giriyor

                trendyol_category_click = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//li[normalize-space(text())="{Category}"]')) #Trendyola kategori ismini giriyor
                )
                trendyol_category_click.click()

                time.sleep(2)

                trendyol_model_kodu = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Model kodu giriniz"]')) #Model kodu kutusuna model kodunu giriyor
                )
                trendyol_model_kodu.send_keys(ModelKodu)

                time.sleep(2)

                marka_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//p[contains(text(),"Marka seçiniz")]')) #Marka kutusuna tıklayıp dropdownu açıyor
                )
                marka_box.click()

                time.sleep(2)

                trendyol_Brand = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Arama"]')) #Sends brand keys to box
                )
                trendyol_Brand.send_keys(Brand)

                time.sleep(2)

                brand_output = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(),"{Brand}")]')) #Chooses the outcome in the dropdown
                )
                brand_output.click()

                Urun_ozellikleri_baslik = driver.find_element(By.XPATH, '//h4[contains(text(),"Ürün Özellikleri")]') #Scrolls to Urun Ozellikleri Headline
                driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", Urun_ozellikleri_baslik)


                if Category == "String":
                    kumas_tipi_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kumaş Tipi"]'))
                    )
                    kumas_tipi_element.click()

                    dantel_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Dantel"]'))
                    )
                    dantel_secenek.click()

                    yas_grubu_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Yaş Grubu"]'))
                    )
                    yas_grubu_element.click()

                    yetiskin_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Yetişkin"]'))
                    )
                    yetiskin_secenek.click()

                    cinsiyet_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Cinsiyet"]'))
                    )
                    cinsiyet_element.click()

                    cinsiyet_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Kadın / Kız"]'))
                    )
                    cinsiyet_secenek.click()

                    bel_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Bel"]'))
                    )
                    bel_element.click()
        
                    bel_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="83"]'))
                    )
                    bel_secenek.click()



                    desen_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Desen"]'))
                    )
                    desen_element.click()
        
                    düz_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Düz"]'))
                    )
                    düz_secenek.click()

                    paket_içeriği_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Paket İçeriği"]'))
                    )
                    paket_içeriği_element.click()
        
                    paket_içeriği_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[4]/div[2]/div[4]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    paket_içeriği_search.send_keys("Tekli")
                    time.sleep(2)
                    paket_içeriği_seçenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[4]/div[2]/div[4]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    paket_içeriği_seçenek.click()

                    kalıp_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kalıp"]'))
                    )
                    kalıp_element.click()
        
                    kalıp_seçenek = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[normalize-space(text())="String"]')) #Sends brand keys to box
                    )
                    kalıp_seçenek.click()

                    ortam_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ortam"]'))
                    )
                    ortam_element.click()
        
                    ortam_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Party"]'))
                    )
                    ortam_secenek.click()
                    
                    ürün_detayı_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ürün Detayı"]'))
                    )
                    ürün_detayı_element.click()
        
                    ürün_detayı_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[4]/div[2]/div[7]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    ürün_detayı_search.send_keys("Dantel Detaylı")
                    time.sleep(2)

                    ürün_detayı_seçenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[4]/div[2]/div[7]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    ürün_detayı_seçenek.click()
                    

                    ek_özellik_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ek Özellik"]'))
                    )
                    ek_özellik_element.click()
        
                    ek_özellik_seçenek = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[normalize-space(text())="Esnek"]')) #Sends brand keys to box
                    )
                    ek_özellik_seçenek.click()

                    koleksiyon_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Koleksiyon"]'))
                    )
                    koleksiyon_element.click()
        
                    koleksiyon_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Basic"]'))
                    )
                    koleksiyon_secenek.click()

                    sürdürülebilirlik_detayı_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Sürdürülebilirlik Detayı"]'))
                    )
                    sürdürülebilirlik_detayı_element.click()
        
                    sürdürülebilirlik_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Evet"]'))
                    )
                    sürdürülebilirlik_secenek.click()

                    menşei_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Menşei"]'))
                    )
                    menşei_element.click()
        
                    menşei_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[11]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    menşei_search.send_keys("TR")
                    time.sleep(2)
                    menşei_seçenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[11]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    menşei_seçenek.click()
                    

                elif Category == "Elbise":
                    boy = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Boy"]'))
                    )
                    boy.click()
                    boy_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="167"]'))
                    )
                    boy_secenek.click()
                    ####
                    kumas_tipi_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kumaş Tipi"]'))
                    )
                    kumas_tipi_element.click()
        
                    dantel_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Tül"]'))
                    )
                    dantel_secenek.click()
                    ####
                    kalıp_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kalıp"]'))
                    )
                    kalıp_element.click()
        
                    kalıp_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    kalıp_search.send_keys("Belirtilmemiş")
                    time.sleep(2)
                    # Try locating the "Belirtilmemiş" option
                    option = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    option.click()
        
                    yas_grubu_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Yaş Grubu"]'))
                    )
                    yas_grubu_element.click()
        
                    yetiskin_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Yetişkin"]'))
                    )
                    yetiskin_secenek.click()
        
                    kol_tipi_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kol Tipi"]'))
                    )
                    kol_tipi_element.click()
        
                    kolsuz_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Kolsuz"]'))
                    )
                    kolsuz_secenek.click()
        
                    materyal_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Materyal"]'))
                    )
                    materyal_element.click()
        
                    tül_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[5]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[5]/span'))
                    )
                    tül_secenek.click()
        
                    desen_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Desen"]'))
                    )
                    desen_element.click()
        
                    düz_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Düz"]'))
                    )
                    düz_secenek.click()
                
                    yaka_tipi_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Yaka Tipi"]'))
                    )
                    yaka_tipi_element.click()
        
                    yaka_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="U Yaka"]'))
                    )
                    yaka_secenek.click()
        
                    kol_boyu_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kol Boyu"]'))
                    )
                    kol_boyu_element.click()
        
                    kol_boyu_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[5]/div[2]/div[5]/div/div/div/div/div/div/div[2]/div[4]/span'))
                    )
                    kol_boyu_secenek.click()
        
                    ortam_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ortam"]'))
                    )
                    ortam_element.click()
        
                    ortam_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Gece"]'))
                    )
                    ortam_secenek.click()
        
        
                    paket_içeriği_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Paket İçeriği"]'))
                    )
                    paket_içeriği_element.click()
        
                    paket_içeriği_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[6]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    paket_içeriği_search.send_keys("Tekli")
                    time.sleep(2)
                    # Try locating the "Belirtilmemiş" option
                    tekli = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[6]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    tekli.click()
        
                    cep_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Cep"]'))
                    )
                    cep_element.click()
        
                    cepsiz_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Cepsiz"]'))
                    )
                    cepsiz_secenek.click()
        
                    kalınlık_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kalınlık"]'))
                    )
                    kalınlık_element.click()
        
                    kalınlık_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="İnce"]'))
                    )
                    kalınlık_secenek.click()
        
                    astar_durumu_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Astar Durumu"]'))
                    )
                    astar_durumu_element.click()
        
                    astarlı_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Astarlı"]'))
                    )
                    astarlı_secenek.click()
        
                    ürün_detayı_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ürün Detayı"]'))
                    )
                    ürün_detayı_element.click()
        
                    ürün_detayı_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[11]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    ürün_detayı_search.send_keys("Dantel")
                    time.sleep(2)
                    # Try locating the "Belirtilmemiş" option
                    ürün_detayı_dantel = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[11]/div/div/div/div/div/div/div[2]/div[3]/span'))
                    )
                    ürün_detayı_dantel.click()
        
                    koleksiyon_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Koleksiyon"]'))
                    )
                    koleksiyon_element.click()
        
                    koleksiyon_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Glam"]'))
                    )
                    koleksiyon_secenek.click()
        
                    persona_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Persona"]'))
                    )
                    persona_element.click()
        
                    persona_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Sexy"]'))
                    )
                    persona_secenek.click()
        
                    siluet_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Siluet"]'))
                    )
                    siluet_element.click()
        
                    siluet_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Slim"]'))
                    )
                    siluet_secenek.click()
        
                    sürdürülebilirlik_detayı_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Sürdürülebilirlik Detayı"]'))
                    )
                    sürdürülebilirlik_detayı_element.click()
        
                    sürdürülebilirlik_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Evet"]'))
                    )
                    sürdürülebilirlik_secenek.click()
        
                    ek_özellik_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Ek Özellik"]'))
                    )
                    ek_özellik_element.click()
        
                    ek_özellik_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[18]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    ek_özellik_search.send_keys("Ek Özellik Mevcut Değil")
                    time.sleep(2)
                    # Try locating the "Belirtilmemiş" option
                    ek_özellik_seçenek = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[18]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    ek_özellik_seçenek.click()
        
                    kemer_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kemer/Kuşak Durumu"]'))
                    )
                    kemer_element.click()
        
                    kemer_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Kemersiz"]'))
                    )
                    kemer_secenek.click()
        
                    yaş_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Yaş"]'))
                    )
                    yaş_element.click()
        
                    yaş_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Tüm Yaş Grupları"]'))
                    )
                    yaş_secenek.click()
        
                    cinsiyet_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Cinsiyet"]'))
                    )
                    cinsiyet_element.click()
        
                    cinsiyet_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Kadın / Kız"]'))
                    )
                    cinsiyet_secenek.click()
        
                    kap_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Kap"]'))
                    )
                    kap_element.click()
        
                    kap_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Kapsız"]'))
                    )
                    kap_secenek.click()
        
                    sezon_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Sezon"]'))
                    )
                    sezon_element.click()
        
                    sezon_secenek = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="Tüm Sezonlar"]'))
                    )
                    sezon_secenek.click()
        
                    menşei_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@data-vv-as="Menşei"]'))
                    )
                    menşei_element.click()
        
                    menşei_search = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[26]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends brand keys to box
                    )
                    time.sleep(2)
                    menşei_search.send_keys("TR")
                    time.sleep(2)
                    # Try locating the "Belirtilmemiş" option
                    menşei_seçenek = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div[26]/div/div/div/div/div/div/div[2]/div[2]/span'))
                    )
                    menşei_seçenek.click()

                urun_acıklaması = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div[4]/div/span')) #Soldaki ürün açıklaması kısmına tıklıyor
                )
                urun_acıklaması.click()

                time.sleep(2)
                ai_acıklama_buton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[6]/div/div/div/div/div[2]/header/button')) #AI açıklama butonuna tıklıyor
                )
                ai_acıklama_buton.click()

                time.sleep(2)

                aciklama_onayla = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[6]/div/div[2]/div[2]/div/div[3]/div/button[2]')) #AI açıklamayı onaylıyor
                )
                aciklama_onayla.click()

                time.sleep(1)

                satis_bilgileri = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div[5]/div/span')) #clicks satış bilgileri on the left
                )
                satis_bilgileri.click()

                time.sleep(3)

                renk_skalası = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div')) #clicks satış bilgileri on the left
                )
                renk_skalası.click()

                time.sleep(3)

                # Define the target color text you want to click
                  # Update this to the color you want to select
                target_color = color

                dropdown_area = driver.find_element(By.CLASS_NAME, "s-content")

                # Initialize a flag to control the loop
                found = False

                # Scroll and search until the target color is found or max attempts are reached
                for _ in range(20):  # Limit the number of scrolls to prevent infinite loop
                    # Locate all items in the dropdown again
                    items = driver.find_elements(By.CSS_SELECTOR, ".s-content .item")

                    for item in items:
                        color_text = item.find_element(By.CLASS_NAME, "text").text

                        # Check if this item matches the target color
                        if color_text == target_color:
                            # Scroll to the item
                            ActionChains(driver).move_to_element(item).perform()
                            time.sleep(0.2)  # Small delay for smoother scrolling

                            # Click the item if it matches and break the loop
                            item.click()
                            print(f"Clicked on color: {color_text}")
                            found = True
                            break
                        
                    # Exit outer loop if item was found
                    if found:
                        break
                    
                    # If target not found, scroll down further
                    dropdown_area.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)  # Delay for smooth scrolling

                if not found:
                    print("Target color not found in dropdown.")


                renk_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/input')) #Sends color keys to box
                )
                renk_input.clear()
                renk_input.send_keys(f"{color}"+f"{color_count}")
                color_count += 1

                Renk_Ekle = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[2]/div[1]/div/div/div/div[1]/button/div')) #clicks size input box
                )
                Renk_Ekle.click()

                Beden_Skalası = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[2]/div[2]/div/div[1]/div/div/div')) #clicks size input box
                )
                Beden_Skalası.click()

                for sku in size_list:
                    try:
                        beden_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/input')) #Sends size keys to box
                        )
                        beden_input.send_keys(sku)
                        size_checkbox = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'text') and text()='{sku}']"))
                        )
                        size_checkbox.click()
                        beden_input.clear()
                    except:
                        beden_input.clear()
                        sku = sku.replace("-","/")
                        beden_input.send_keys(sku)
                        size_checkbox = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'text') and text()='{sku}']"))
                        )
                        size_checkbox.click()
                        beden_input.clear()
                        continue

                satış_bilgileri = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div[5]/div/span')) #clicks size input box
                )
                satış_bilgileri.click()

                time.sleep(2)

                satis_fiyati_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/input')) #Sends size keys to box
                )
                satis_fiyati_input.send_keys(Keys.HOME)
                satis_fiyati_input.send_keys(formatted_price)

                kdv_rate = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[3]/div/div/div[2]/div/div/div/div/div')) #clicks size input box
                )
                kdv_rate.click()

                kdv_10 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[3]/span')) #clicks size input box
                )
                kdv_10.click()

                time.sleep(3)

                all_checkbox = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[4]/div[1]/table/thead/tr/th[1]/div/label')) #clicks size implement to all checkbox
                )
                all_checkbox.click()

                tümüne_uygula = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[3]/div/div/div[4]/button/div')) #clicks to tümüne uygula button
                )
                tümüne_uygula.click()

                Image_Upload_Button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[4]/div[1]/table/tbody/tr[1]/td[2]/div/div/div')) #görsel yükleme butonuna tıklıyor
                )
                Image_Upload_Button.click()


                file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[5]/div[2]/div/div[2]/div[2]/div[1]/div[1]/input"))
                )

                file_paths = images[index]

                files_path_string = "\n".join(file_paths) # Join all items in the list with a newline character to simulate multiple file selection, this is the how its done in selenium.

                print(file_paths)

                file_input.send_keys(files_path_string)
                time.sleep(1)  # Delay in seconds, adjust as needed

                Görselleri_Yükle_Button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[8]/div/div[5]/div[2]/div/div[2]/div[2]/div[2]/div[2]/button[2]')) #popup görselleri yükle butonu
                )

                time.sleep(3)
                Görselleri_Yükle_Button.click()

                # Generate a random alphanumeric value
                def generate_random_value(length=8):
                    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

                # Locate elements with a partial match
                barcode_fields = driver.find_elements(By.XPATH, "//input[contains(@name, 'barcode')]")

                for field in barcode_fields:
                    random_value = generate_random_value()
                    field.send_keys(random_value)


                stok_fields = driver.find_elements(By.XPATH, "//input[contains(@name, 'quantity')]")

                stok_index = 0

                # Iterate through the found fields and send stock values to each one, excluding the 4th input field
                for field in stok_fields:
                    # Skip the field with name 'bulkUpdate_quantity' (1st input)
                    if field.get_attribute("name") == "bulkUpdate_quantity":
                        print(f"Skipping field with name '{field.get_attribute('name')}'.")
                        continue
                    
                    # Ensure there's still a stock value left to assign
                    if stok_index < len(stok_adedi_list):
                        field.send_keys(str(stok_adedi_list[stok_index]))
                        print(f"Sent value '{stok_adedi_list[stok_index]}' to field {stok_index+1}")
                        stok_index += 1  # Move to the next stock value
                    else:
                        print("No more stock values to send.")


                stock_code_fields = driver.find_elements(By.XPATH, "//input[contains(@name, 'stockCode')]")

                for sku,field in enumerate(stock_code_fields):
                    field.send_keys(stok_kodu_list[sku])

                time.sleep(3)

                Ürünü_Onaya_Gönder_Button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/footer/div/button')) #en sondaki ürünü onaya gönder butonu
                )

                Ürünü_Onaya_Gönder_Button.click()

                Yoksay_ve_Devamet_Button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/div/div[3]/button[1]')) #ürünü onaya göndere basınca çıkan popupdaki yoksay ve devam et butonu
                )

                Yoksay_ve_Devamet_Button.click()

                time.sleep(3)


            except Exception as e:
                print(f"Error interacting with Trendyol elements: {e}")

            driver.switch_to.window(driver.window_handles[1])


        # Optional: Verify and print cookies

        # Close the browser
        time.sleep(60)
        driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SeleniumAutomationGUI()
    gui.show()
    sys.exit(app.exec_())


