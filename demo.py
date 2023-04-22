import sys
import socket
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTextEdit, QProgressBar, QTabWidget, QComboBox


class FirewallDetector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets
        title_label = QLabel('Firewall Detector')
        ip_label = QLabel('IP Address:')
        self.ip_input = QLineEdit()
        port_label = QLabel('Port Range:')
        self.start_port_input = QLineEdit()
        self.start_port_input.setFixedWidth(80)
        self.end_port_input = QLineEdit()
        self.end_port_input.setFixedWidth(80)
        detect_button = QPushButton('Detect Firewall')
        self.result_label = QLabel('')
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)

        # Add widgets to layout
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(ip_label)
        hbox1.addWidget(self.ip_input)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(port_label)
        hbox2.addWidget(self.start_port_input)
        hbox2.addWidget(QLabel('-'))
        hbox2.addWidget(self.end_port_input)
        vbox.addLayout(hbox2)
        vbox.addWidget(detect_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.result_text)
        vbox.addWidget(self.progress_bar)

        self.setLayout(vbox)
        self.setWindowTitle('Firewall Detector')

        # Connect buttons to methods
        detect_button.clicked.connect(self.detect_firewall)

    def detect_firewall(self):
        ip_address = self.ip_input.text()
        start_port = int(self.start_port_input.text())
        end_port = int(self.end_port_input.text())
        self.result_text.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(end_port - start_port + 1)
        self.result_label.setText('Scanning ports...')
        self.result_label.repaint()
        open_ports = []
        for port in range(start_port, end_port + 1):
            try:
                self.progress_bar.setValue(port - start_port + 1)
                self.result_text.insertPlainText('Checking port {}: '.format(port))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    self.result_text.insertPlainText('OPEN\n')
                    open_ports.append(port)
                else:
                    self.result_text.insertPlainText('CLOSED\n')
                s.close()
            except socket.error:
                self.result_text.insertPlainText('ERROR\n')
        if open_ports:
            self.result_label.setText('Firewall Detected!')
            self.result_label.setStyleSheet('color: red')
        else:
            self.result_label.setText('No Firewall Detected')
            self.result_label.setStyleSheet('color: green')


class WebScraper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets
        title_label = QLabel('Web Scraper')
        url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        self.extract_label = QLabel('Extract:')
        self.extract_combo = QComboBox()
        self.extract_combo.addItem('Links')
        self.extract_combo.addItem('Images')
        self.extract_combo.addItem('JavaScript Files')
        scrape_button = QPushButton('Scrape Website')
        self.result_label = QLabel('')
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)

        # Add widgets to layout
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(url_label)
        hbox1.addWidget(self.url_input)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.extract_label)
        hbox2.addWidget(self.extract_combo)
        vbox.addLayout(hbox2)
        vbox.addWidget(scrape_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.result_text)
        vbox.addWidget(self.progress_bar)

        self.setLayout(vbox)
        self.setWindowTitle('Web Scraper')

        # Connect buttons to methods
        scrape_button.clicked.connect(self.scrape_website)

    def scrape_website(self):
        url = self.url_input.text()
        self.result_text.clear()
        self.progress_bar.setValue(0)
        self.result_label.setText('Scraping website...')
        self.result_label.repaint()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if self.extract_combo.currentText() == 'Links':
                extracted_elements = [link.get('href') for link in soup.find_all('a') if link.get('href') is not None]
            elif self.extract_combo.currentText() == 'Images':
                extracted_elements = [img.get('src') for img in soup.find_all('img') if img.get('src') is not None]
            else:
                extracted_elements = [script.get('src') for script in soup.find_all('script') if script.get('src') is not None and script.get('src').endswith('.js')]
            self.result_text.insertPlainText('\n'.join(extracted_elements))
            self.result_label.setText('Elements Extracted Successfully')
            self.result_label.setStyleSheet('color: green')
        except Exception as e:
            self.result_label.setText(str(e))
            self.result_label.setStyleSheet('color: red')

    def change_tab(self, index):
        if index == 1:
            self.parent().setCurrentIndex(1) # index of the Firewall Detector tab is 1
if __name__ == '__main__':
    app = QApplication(sys.argv)
    tabs = QTabWidget()
    firewall_detector = FirewallDetector()
    web_scraper = WebScraper()
    tabs.addTab(web_scraper, 'Web Scraper')
    tabs.addTab(firewall_detector, 'Firewall Detector')
    tabs.resize(610, 400)
    tabs.show()
    sys.exit(app.exec_())

