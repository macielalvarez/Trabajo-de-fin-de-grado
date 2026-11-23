import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


LOGIN_URL = "http://riegos.ivia.es/acceso-al-area-personal"
URL_DATOS = "http://riegos.ivia.es/datos-meteorologicos"

DOWNLOAD_DIR = os.path.join(os.getcwd(), "ivia_descargas2")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


PERIODOS = [
    ("01/01/2020", "30/06/2020"),
    ("01/07/2020", "31/12/2020"),
    ("01/01/2021", "30/06/2021"),
    ("01/07/2021", "31/12/2021"),
    ("01/01/2022", "30/06/2022"),
    ("01/07/2022", "31/12/2022"),
    ("01/01/2023", "30/06/2023"),
    ("01/07/2023", "31/12/2023"),
    ("01/01/2024", "30/06/2024"),
    ("01/07/2024", "31/12/2024"),
]

TIEMPO_CALCULO = 70
CSV_TIMEOUT = 130

IVIA_USER = os.getenv("IVIA_USER", "ivia_user")
IVIA_PASS = os.getenv("IVIA_PASS", "ivia_pass")

chrome_opts = Options()
chrome_opts.add_argument("--no-sandbox")
chrome_opts.add_argument("--disable-dev-shm-usage")
chrome_opts.add_argument("--window-size=1920,1080")
chrome_opts.add_argument("--disable-gpu")
chrome_opts.add_argument("--disable-extensions")


prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_opts.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
wait = WebDriverWait(driver, 40)

def wait_for_csv_file(timeout=CSV_TIMEOUT):
    start = time.time()
    seen = set(os.listdir(DOWNLOAD_DIR))
    while time.time() - start < timeout:
        cur = set(os.listdir(DOWNLOAD_DIR))
        added = cur - seen
        csvs = [f for f in added if f.lower().endswith(".csv")]
        if csvs:
            return os.path.join(DOWNLOAD_DIR, sorted(csvs)[0])
        time.sleep(1)
    return None


def set_date(elem, value):
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        elem, value
    )
    time.sleep(0.3)


try:
    print(" Abriendo página de inicio de sesión...")
    driver.get(LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    print(" Introduciendo credenciales...")
    user_input = wait.until(EC.presence_of_element_located((By.ID, "login")))
    pass_input = wait.until(EC.presence_of_element_located((By.ID, "clave")))
    btn_enviar = wait.until(EC.presence_of_element_located((By.ID, "enviar")))

    user_input.send_keys(IVIA_USER)
    pass_input.send_keys(IVIA_PASS)
    btn_enviar.click()

    print(" Iniciando sesión...")
    time.sleep(5)

    if "acceso" in driver.current_url.lower():
        raise RuntimeError("Error: no se ha iniciado sesión correctamente.")

    print("Sesión iniciada correctamente.")

    print(" Accediendo directamente a /datos-meteorologicos ...")
    driver.get(URL_DATOS)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)
    print(" URL actual:", driver.current_url)

    print(" Esperando selector de cultivo...")
    boton_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.ui-multiselect")))
    driver.execute_script("arguments[0].click();", boton_selector)
    time.sleep(1.0)

    opciones = driver.find_elements(By.CSS_SELECTOR, "label[for^='ui-multiselect-cultivo-option']")
    for op in opciones:
        if "Viña Vino" in op.text or "Viña" in op.text:
            driver.execute_script("arguments[0].click();", op)
            break
    driver.execute_script("arguments[0].click();", boton_selector)
    print("Cultivo 'Viña Vino' seleccionado.")

    print(" Seleccionando estación '...'...")
    tabla = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table, div.table")))
    filas = tabla.find_elements(By.TAG_NAME, "tr")
    for fila in filas:
        if "Camp de Mirra" in fila.text:
            chk = fila.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            driver.execute_script("arguments[0].click();", chk)
            break

    try:
        btn_sel = driver.find_element(By.ID, "seleccionar")
        driver.execute_script("arguments[0].click();", btn_sel)
    except Exception:
        pass
    print(" Estación seleccionada.")

    print(" Seleccionando rango temporal...")
    rango_sel = wait.until(EC.presence_of_element_located((By.ID, "rango_temporal")))
    Select(rango_sel).select_by_visible_text("Semihorarios")

    inicio_el = wait.until(EC.element_to_be_clickable((By.ID, "inicio")))
    fin_el = wait.until(EC.element_to_be_clickable((By.ID, "fin")))

    csv_paths = []
    for fecha_i, fecha_f in PERIODOS:
        print(f" Descargando periodo {fecha_i} → {fecha_f}")
        set_date(inicio_el, fecha_i)
        set_date(fin_el, fecha_f)

        fin_input = driver.find_element(By.ID, "fin")
        driver.execute_script("arguments[0].click();", fin_input)
        print(" Click en el campo de fecha de fin para actualizar días...")

        time.sleep(1)

        btn_calc = driver.find_element(By.ID, "calcular")
        driver.execute_script("arguments[0].click();", btn_calc)
        print(f" Calculando... Esperando {TIEMPO_CALCULO}s...")
        time.sleep(TIEMPO_CALCULO)

        enlace_csv = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.formato_csv")))
        driver.execute_script("arguments[0].click();", enlace_csv)
        print("Descargando CSV...")

        csv_file = wait_for_csv_file()
        if not csv_file:
            raise RuntimeError("No se descargó el CSV.")
        csv_paths.append(csv_file)
        print(f" CSV guardado: {csv_file}")

    driver.quit()

    print(" Combinando CSVs...")

    dfs = []
    for i, p in enumerate(csv_paths):
        print(f" Procesando CSV {i+1}: {p}")
        df = pd.read_csv(p, sep=";", encoding="utf-8-sig", on_bad_lines="skip", skip_blank_lines=True)
        header = list(df.columns)
        df = df[~df.apply(lambda row: all(str(row[col]) == header[idx] for idx, col in enumerate(df.columns)), axis=1)]
        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)
    out_final = os.path.join(DOWNLOAD_DIR, "datos_vina_vino_2020_2024.csv")
    df_final.to_csv(out_final, index=False, sep=";", encoding="utf-8-sig")

    print(f" Archivo final generado: {out_final}")
    print(" Primeras filas del resultado:")
    print(df_final.head())

except Exception as e:
    print(" Error:", e)
    driver.quit()
