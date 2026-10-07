import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, 
    QLineEdit, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt
from app.styles import MAIN_STYLE

from document.word_reader import extract_text_from_docx, save_text_to_docx
from crypto.key_derivation import generate_salt, derive_key
from crypto.encryption import encrypt_data
from crypto.decryption import decrypt_data
from storage.encrypted_file import pack_encrypted_data, unpack_encrypted_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES Word Encryptor")
        self.resize(800, 600)
        self.setStyleSheet(MAIN_STYLE)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Title Label
        title = QLabel("🛡️ AES Word Encryptor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title)
        
        self.tabs = QTabWidget()
        self.tab_encrypt = QWidget()
        self.tab_decrypt = QWidget()
        
        self.tabs.addTab(self.tab_encrypt, "🔒 Enkripsi")
        self.tabs.addTab(self.tab_decrypt, "🔓 Dekripsi")
        
        self.layout.addWidget(self.tabs)
        
        self.setup_encrypt_tab()
        self.setup_decrypt_tab()

    def setup_encrypt_tab(self):
        layout = QVBoxLayout(self.tab_encrypt)
        
        # File selection
        file_layout = QHBoxLayout()
        self.lbl_enc_file = QLabel("File Input (.docx): Belum dipilih")
        self.btn_enc_browse = QPushButton("📂 Pilih File Word")
        self.btn_enc_browse.clicked.connect(self.browse_docx)
        file_layout.addWidget(self.lbl_enc_file)
        file_layout.addStretch()
        file_layout.addWidget(self.btn_enc_browse)
        layout.addLayout(file_layout)
        
        # Text display
        layout.addWidget(QLabel("Plaintext / Ciphertext Preview:"))
        self.txt_enc_preview = QTextEdit()
        self.txt_enc_preview.setReadOnly(True)
        layout.addWidget(self.txt_enc_preview)
        
        # Password
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("Password:"))
        self.input_enc_pwd = QLineEdit()
        self.input_enc_pwd.setEchoMode(QLineEdit.Password)
        pwd_layout.addWidget(self.input_enc_pwd)
        layout.addLayout(pwd_layout)
        
        # Actions
        action_layout = QHBoxLayout()
        self.btn_encrypt = QPushButton("🔒 ENKRIPSI")
        self.btn_encrypt.clicked.connect(self.process_encrypt)
        self.btn_enc_save = QPushButton("💾 Simpan Hasil (.docx)")
        self.btn_enc_save.clicked.connect(self.save_enc_docx)
        self.btn_enc_save.setEnabled(False)
        
        action_layout.addStretch()
        action_layout.addWidget(self.btn_encrypt)
        action_layout.addWidget(self.btn_enc_save)
        layout.addLayout(action_layout)
        
        self.current_docx_path = None
        self.current_plaintext = None
        self.current_ciphertext_data = None

    def setup_decrypt_tab(self):
        layout = QVBoxLayout(self.tab_decrypt)
        
        # File selection
        file_layout = QHBoxLayout()
        self.lbl_dec_file = QLabel("File Input (.docx): Belum dipilih")
        self.btn_dec_browse = QPushButton("📂 Pilih File Terenkripsi (.docx)")
        self.btn_dec_browse.clicked.connect(self.browse_enc)
        file_layout.addWidget(self.lbl_dec_file)
        file_layout.addStretch()
        file_layout.addWidget(self.btn_dec_browse)
        layout.addLayout(file_layout)
        
        # Text display
        layout.addWidget(QLabel("Plaintext Preview:"))
        self.txt_dec_preview = QTextEdit()
        self.txt_dec_preview.setReadOnly(True)
        layout.addWidget(self.txt_dec_preview)
        
        # Password
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("Password:"))
        self.input_dec_pwd = QLineEdit()
        self.input_dec_pwd.setEchoMode(QLineEdit.Password)
        pwd_layout.addWidget(self.input_dec_pwd)
        layout.addLayout(pwd_layout)
        
        # Actions
        action_layout = QHBoxLayout()
        self.btn_decrypt = QPushButton("🔓 DEKRIPSI")
        self.btn_decrypt.clicked.connect(self.process_decrypt)
        
        self.btn_dec_save = QPushButton("💾 Simpan Hasil (.docx)")
        self.btn_dec_save.clicked.connect(self.save_dec_docx)
        self.btn_dec_save.setEnabled(False)

        action_layout.addStretch()
        action_layout.addWidget(self.btn_decrypt)
        action_layout.addWidget(self.btn_dec_save)
        layout.addLayout(action_layout)
        
        self.current_enc_path = None
        self.current_decrypted_text = None

    def browse_docx(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File Word", "", "Word Documents (*.docx)")
        if file_name:
            try:
                self.current_docx_path = file_name
                self.lbl_enc_file.setText(f"File: {os.path.basename(file_name)}")
                self.current_plaintext = extract_text_from_docx(file_name)
                self.txt_enc_preview.setPlainText(self.current_plaintext)
                self.current_ciphertext_data = None
                self.btn_enc_save.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def process_encrypt(self):
        if not self.current_plaintext:
            QMessageBox.warning(self, "Peringatan", "Pilih file Word terlebih dahulu.")
            return
            
        password = self.input_enc_pwd.text()
        if not password:
            QMessageBox.warning(self, "Peringatan", "Password tidak boleh kosong.")
            return
            
        try:
            iterations = 480000
            salt = generate_salt()
            key = derive_key(password, salt, iterations)
            
            plaintext_bytes = self.current_plaintext.encode('utf-8')
            nonce, ciphertext, tag = encrypt_data(key, plaintext_bytes)
            
            self.current_ciphertext_data = (iterations, salt, nonce, tag, ciphertext)
            
            b64_preview = pack_encrypted_data(iterations, salt, nonce, tag, ciphertext)
            self.txt_enc_preview.setPlainText(f"[ENCRYPTED PREVIEW BASE64]\n{b64_preview[:1000]}...")
            
            self.btn_enc_save.setEnabled(True)
            QMessageBox.information(self, "Sukses", "Enkripsi berhasil. Silakan simpan hasilnya.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Enkripsi gagal: {str(e)}")

    def save_enc_docx(self):
        if not self.current_ciphertext_data:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(self, "Simpan File Word Terenkripsi", "", "Word Documents (*.docx)")
        if file_name:
            try:
                iterations, salt, nonce, tag, ciphertext = self.current_ciphertext_data
                b64_data = pack_encrypted_data(iterations, salt, nonce, tag, ciphertext)
                save_text_to_docx(b64_data, file_name)
                QMessageBox.information(self, "Sukses", "File terenkripsi berhasil disimpan dalam format Word (.docx).")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan file: {str(e)}")

    def browse_enc(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File Terenkripsi Word", "", "Word Documents (*.docx)")
        if file_name:
            try:
                self.current_enc_path = file_name
                self.lbl_dec_file.setText(f"File: {os.path.basename(file_name)}")
                
                # Preview base64 text
                b64_data = extract_text_from_docx(file_name).strip()
                self.txt_dec_preview.setPlainText(f"[ENCRYPTED DATA]\n{b64_data[:1000]}...")
                
                self.btn_dec_save.setEnabled(False)
                self.current_decrypted_text = None
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal membaca file: {str(e)}")

    def process_decrypt(self):
        if not self.current_enc_path:
            QMessageBox.warning(self, "Peringatan", "Pilih file terenkripsi terlebih dahulu.")
            return
            
        password = self.input_dec_pwd.text()
        if not password:
            QMessageBox.warning(self, "Peringatan", "Password tidak boleh kosong.")
            return
            
        try:
            # 1. Extract base64 text from the docx
            b64_data = extract_text_from_docx(self.current_enc_path).strip()
            
            # 2. Unpack
            iterations, salt, nonce, tag, ciphertext = unpack_encrypted_data(b64_data)
            
            # 3. Derive key and decrypt
            key = derive_key(password, salt, iterations)
            plaintext_bytes = decrypt_data(key, nonce, tag, ciphertext)
            plaintext = plaintext_bytes.decode('utf-8')
            
            self.current_decrypted_text = plaintext
            self.txt_dec_preview.setPlainText(plaintext)
            self.btn_dec_save.setEnabled(True)
            QMessageBox.information(self, "Sukses", "Dekripsi berhasil. Silakan simpan hasilnya.")
        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Dekripsi Gagal: {str(e)}")

    def save_dec_docx(self):
        if not self.current_decrypted_text:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(self, "Simpan Hasil Dekripsi", "", "Word Documents (*.docx)")
        if file_name:
            try:
                save_text_to_docx(self.current_decrypted_text, file_name)
                QMessageBox.information(self, "Sukses", "File hasil dekripsi berhasil disimpan dalam format Word (.docx).")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan file: {str(e)}")
