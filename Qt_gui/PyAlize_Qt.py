from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QTableView, QComboBox, QStyledItemDelegate,
    QSpinBox, QDoubleSpinBox, QHeaderView,
    QFileDialog, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from PySide6.QtCore import Qt, Signal
import csv
import os
import sys
sys.path.append(os.getcwd())

from qt_material import apply_stylesheet  # Feuille de style Material
from classes.class_struct import structure, layer
from classes.run import run_roue_simple, run_jumelage


# --- Délégué ComboBox ---
class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.items)
        combo.currentIndexChanged.connect(lambda: self.commitData.emit(combo))
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value:
            i = editor.findText(value)
            if i >= 0:
                editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)


# --- Délégué pour les entiers ---
class IntDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        spin = QSpinBox(parent)
        spin.setRange(0, 1_000_000_000)
        spin.setSingleStep(100)
        return spin

    def setEditorData(self, editor, index):
        try:
            v = index.model().data(index, Qt.EditRole)
            editor.setValue(int(v))
        except:
            editor.setValue(0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.EditRole)


# --- Délégué pour les floats ---
class FloatDelegate(QStyledItemDelegate):
    def __init__(self, decimals=4, min_val=0.0, max_val=1_000_000.0, step=0.001, parent=None):
        super().__init__(parent)
        self.decimals = decimals
        self.min_val = min_val
        self.max_val = max_val
        self.step = step

    def createEditor(self, parent, option, index):
        spin = QDoubleSpinBox(parent)
        spin.setDecimals(self.decimals)
        spin.setRange(self.min_val, self.max_val)
        spin.setSingleStep(self.step)
        return spin

    def setEditorData(self, editor, index):
        try:
            v = index.model().data(index, Qt.EditRole)
            editor.setValue(float(v))
        except:
            editor.setValue(0.0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.EditRole)


# --- TableStruct ---
class TableStruct(QTableView):
    rows_count_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Modèle
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "nom",
            "épaisseur",
            "module",
            "coefficient\n de poisson",
            "interface"
        ])

        # Exemple de données
        data = [
            ["BB", 0.06, 7000, 0.35, "Collée"],
            ["GB4", 0.13, 11000, 0.35, "Collée"],
            ["CdF", None, 50, 0.35, "Collée"],
        ]
        for row in data:
            self._append_row(row)

        self.setModel(self.model)

        # Délégués
        self.setItemDelegateForColumn(1, FloatDelegate(decimals=3, min_val=0.0, max_val=1000.0, step=0.001)) # épaisseur
        self.setItemDelegateForColumn(2, IntDelegate()) # Module
        self.setItemDelegateForColumn(3, FloatDelegate(decimals=2, min_val=0.0, max_val=1.0, step=0.01)) # poisson
        self.setItemDelegateForColumn(4, ComboBoxDelegate(["Collée", "Glissante"], self))

        # Configuration des en-têtes
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        header.setDefaultSectionSize(150)  # largeur des colonnes
        header.setFixedHeight(50) 
        header.setDefaultAlignment(Qt.AlignCenter)

        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QTableView.DoubleClicked | QTableView.SelectedClicked)

        self.model.rowsInserted.connect(self.rows_changed)
        self.model.rowsRemoved.connect(self.rows_changed)
        self.rows_changed()

    def _create_items(self, values=None):
        if values is None:
            values = ["", 0.0, 0, 0.0, "Collée"]
        items = [QStandardItem(str(v)) for v in values]
        for i in [1, 2, 3]:
            items[i].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return items

    def _append_row(self, values=None):
        self.model.appendRow(self._create_items(values))

    def add_row(self):
        sel = self.selectionModel().selectedRows()
        if sel:
            target = sel[0].row()
            self.model.insertRow(target, self._create_items())
        else:
            self._append_row()

    def remove_selected_row(self):
        sel = self.selectionModel().selectedRows()
        for idx in sorted(sel, key=lambda x: x.row(), reverse=True):
            self.model.removeRow(idx.row())

    def export_to_csv(self, filename):
        headers = [self.model.headerData(i, Qt.Horizontal) for i in range(self.model.columnCount())]
        with open(filename, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r in range(self.model.rowCount()):
                writer.writerow([
                    self.model.item(r, c).text() if self.model.item(r, c) else ""
                    for c in range(self.model.columnCount())
                ])

    def export_struct(self) :
        # exporte les données sous forme d'un objet structure
        struct = structure()
        for r in range(self.model.rowCount()):

            nom = self.model.item(r , 0).text()
            if r == self.model.rowCount() -1 :
                ep = 0
            else :
                ep = self.model.item(r, 1).text()
            module = self.model.item(r, 2).text()
            nu = self.model.item(r, 3).text()
            inter = self.model.item(r,4).text()
            if inter == 'Collée' or inter == 'colléé' :
                inter = True
            else :
                inter = False
            a_layer = layer()
            a_layer.define(nom, float(ep), int(module), float(nu), inter, r)
            struct.add_layer(a_layer)
            a_layer = None

        return struct



    def highlight_last_row(self): # pour masquer l'épaisseur et l'interface
        rc = self.model.rowCount()
        if rc == 0:
            return
        last = rc - 1
        for col in [1, 4]:
            item = self.model.item(last, col)
            if item:
                gris = QColor(250, 250, 250)
                #item.setBackground(gris)
                #item.setForeground(gris)  # texte invisible
                item.setFlags(item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsEnabled)

        # Réactiver les autres lignes
        for row in range(last):
            for col in [1, 4]:
                item = self.model.item(row, col)
                if item:
                    item.setBackground(Qt.white)
                    item.setForeground(Qt.black)
                    item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsEnabled)

    def rows_changed(self):
        self.rows_count_changed.emit(self.model.rowCount())
        self.highlight_last_row()

    def validate_data(self):
        erreurs = []
        rc = self.model.rowCount()
        for row in range(rc):
            nom_item = self.model.item(row, 0)
            ep_item = self.model.item(row, 1)
            mod_item = self.model.item(row, 2)
            coeff_item = self.model.item(row, 3)

            if not nom_item or not nom_item.text().strip():
                erreurs.append(f"Ligne {row+1} : nom non renseigné")

            if row != rc - 1:
                try:
                    if float(ep_item.text()) <= 0:
                        erreurs.append(f"Ligne {row+1} : épaisseur doit être > 0")
                except:
                    erreurs.append(f"Ligne {row+1} : épaisseur invalide")

            try:
                if int(float(mod_item.text())) <= 0:
                    erreurs.append(f"Ligne {row+1} : module doit être > 0")
            except:
                erreurs.append(f"Ligne {row+1} : module invalide")

            try:
                if float(coeff_item.text()) <= 0:
                    erreurs.append(f"Ligne {row+1} : coefficient doit être > 0")
            except:
                erreurs.append(f"Ligne {row+1} : coefficient invalide")

        return len(erreurs) == 0, erreurs


# --- Fenêtre principale ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableStruct - Matériaux")

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # Tableau + boutons droite
        table_layout = QHBoxLayout()
        self.table = TableStruct()
        table_layout.addWidget(self.table)

        right_btn_layout = QVBoxLayout()
        self.btn_import = QPushButton("📂 Importer CSV")
        self.btn_export = QPushButton("💾 Exporter CSV")
        self.btn_add = QPushButton("➕ Ajouter une ligne")
        self.btn_remove = QPushButton("🗑️ Supprimer la ligne")
        right_btn_layout.addWidget(self.btn_import)
        right_btn_layout.addWidget(self.btn_export)
        right_btn_layout.addWidget(self.btn_add)
        right_btn_layout.addWidget(self.btn_remove)
        right_btn_layout.addStretch()
        table_layout.addLayout(right_btn_layout)
        main_layout.addLayout(table_layout)

        # Boutons en dessous
        bottom_layout = QHBoxLayout()
        left_bot = QHBoxLayout()
        self.btn_calcul1 = QPushButton("Calcul Roue simple")
        self.btn_calcul2 = QPushButton("Calcul Jumelage")
        left_bot.addWidget(self.btn_calcul1)
        left_bot.addWidget(self.btn_calcul2)
        bottom_layout.addLayout(left_bot)

        bottom_layout.addStretch()
        self.btn_close = QPushButton("Fermer")
        bottom_layout.addWidget(self.btn_close)
        main_layout.addLayout(bottom_layout)

        self.setCentralWidget(central)

        # Connections
        self.btn_add.clicked.connect(self.table.add_row)
        self.btn_remove.clicked.connect(self.table.remove_selected_row)
        self.btn_export.clicked.connect(self.export_csv)
        self.btn_import.clicked.connect(self.import_csv)
        self.btn_calcul1.clicked.connect(self.calcul1)
        self.btn_calcul2.clicked.connect(self.calcul2)
        self.btn_close.clicked.connect(self.close)
        self.table.rows_count_changed.connect(self.update_delete_button_state)
        self.update_delete_button_state(self.table.model.rowCount())

    def update_delete_button_state(self, row_count: int):
        self.btn_remove.setEnabled(row_count > 2)

    def export_csv(self):
        valid, erreurs = self.table.validate_data()
        if not valid:
            QMessageBox.warning(
                self,
                "Erreur de validation",
                "Impossible d'exporter le CSV :\n" + "\n".join(erreurs)
            )
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Exporter le tableau en CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*.*)")
        if filename:
            try:
                self.table.export_to_csv(filename)
                QMessageBox.information(self, "Export réussi", f"Le tableau a été exporté vers :\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de l'export CSV : {e}")

    def import_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Importer un tableau CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*.*)")
        if not filename:
            return
        try:
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows or len(rows) < 2:
                    QMessageBox.warning(self, "Erreur CSV", "Fichier vide ou invalide")
                    return
                headers = rows[0]
                expected = ["nom", "épaisseur", "module", "coefficient\n de poisson", "interface"]
                if headers != expected:
                    QMessageBox.warning(self, "Erreur CSV", f"Colonnes attendues : {expected}")
                    return
                new_data = []
                for line in rows[1:]:
                    if len(line) != 5:
                        raise ValueError("Nombre de colonnes incorrect")
                    nom = str(line[0])
                    ep = float(line[1])
                    mo = int(float(line[2]))
                    cf = float(line[3])
                    interf = line[4].strip()
                    if interf not in ["Collée", "Glissante"]:
                        raise ValueError(f"Interface invalide : {interf}")
                    new_data.append([nom, ep, mo, cf, interf])
                self.table.model.removeRows(0, self.table.model.rowCount())
                for row in new_data:
                    self.table._append_row(row)
        except Exception as e:
            QMessageBox.critical(self, "Erreur CSV", f"Impossible d'importer le CSV : {e}")
    
    # --- Fonctions de calculs ---
    def collect_data(self) :
        valid, erreurs = self.table.validate_data()
        if not valid:
            QMessageBox.warning(
                self,
                "Erreur de validation",
                "Impossible de lancer les calculs :\n" + "\n".join(erreurs)
            )
            return

        struct = self.table.export_struct()
        struct.calc_struct()
        
        return struct


    def calcul1(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Exporter les résulats", "", "Fichiers TXT (*.txt;;Tous les fichiers (*.*)")
        if filename:
            try:
                struct = self.collect_data()
                run_roue_simple(struct, filename)


                QMessageBox.information(self, "Calculs réussis !", f"Les résulats a été exporté vers :\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Echec des calculs : {e}")



    def calcul2(self):

        filename, _ = QFileDialog.getSaveFileName(self, "Exporter les résulats", "",
                                                  "Fichiers TXT (*.txt;;Tous les fichiers (*.*)")
        if filename:
            try:
                struct = self.collect_data()
                run_jumelage(struct, filename)
                QMessageBox.information(self, "Calculs réussis !", f"Les résulats a été exporté vers :\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Echec des calculs : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Appliquer le thème Qt-Material
    apply_stylesheet(app, theme="dark_pink.xml")

    window = MainWindow()
    window.resize(1050, 400)
    window.show()
    sys.exit(app.exec())
