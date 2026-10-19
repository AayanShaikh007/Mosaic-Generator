"""Desktop interface for the image mosaic generator."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import mosaic


class MosaicInterface(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.selected_target: Path | None = None
        self.setWindowTitle("Mosaic Generator")
        self.resize(960, 620)
        self._build_ui()
        self._set_preview(mosaic.ASSETS_DIR / "placeholder.png")

    def _build_ui(self) -> None:
        self.source_box = QComboBox()
        self.source_box.addItem("Choose a source collection", None)
        self.source_box.addItem("Real-world images", mosaic.real_path)
        self.source_box.addItem("Solid colors", mosaic.static_path)

        self.target_box = QComboBox()
        self.target_box.addItem("Choose a sample target", None)
        for index in range(1, 5):
            self.target_box.addItem(
                f"Sample {index}", mosaic.ASSETS_DIR / "targets" / f"target{index}.jpg"
            )
        self.target_box.currentIndexChanged.connect(self._sample_selected)

        self.rows_box = QSpinBox()
        self.rows_box.setRange(1, 1080)
        self.rows_box.setValue(60)
        self.columns_box = QSpinBox()
        self.columns_box.setRange(1, 1920)
        self.columns_box.setValue(100)

        self.upload_button = QPushButton("Choose target image...")
        self.upload_button.clicked.connect(self._choose_target)
        self.generate_button = QPushButton("Generate mosaic")
        self.generate_button.clicked.connect(self._generate)
        self.view_button = QPushButton("Open full-size result")
        self.view_button.clicked.connect(self._view_result)
        self.status_label = QLabel("Choose a source collection and target image.")
        self.status_label.setWordWrap(True)

        options = QFormLayout()
        options.addRow("Source collection", self.source_box)
        options.addRow("Sample target", self.target_box)
        options.addRow("Rows", self.rows_box)
        options.addRow("Columns", self.columns_box)

        controls = QVBoxLayout()
        controls.addLayout(options)
        controls.addWidget(self.upload_button)
        controls.addWidget(self.generate_button)
        controls.addWidget(self.view_button)
        controls.addWidget(self.status_label)
        control_group = QGroupBox("Mosaic settings")
        control_group.setLayout(controls)

        self.preview = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumSize(560, 360)
        self.preview.setStyleSheet("background: #20252b; border: 1px solid #4b5563;")
        layout = QGridLayout(self)
        layout.addWidget(control_group, 0, 0)
        layout.addWidget(self.preview, 0, 1)
        layout.setColumnStretch(1, 1)

    def _sample_selected(self) -> None:
        target = self.target_box.currentData()
        if target is not None:
            self.selected_target = Path(target)
            self.status_label.setText(f"Target selected: {self.selected_target.name}")

    def _choose_target(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choose target image",
            str(mosaic.ASSETS_DIR),
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if filename:
            self.selected_target = Path(filename)
            self.target_box.setCurrentIndex(0)
            self.status_label.setText(f"Target selected: {self.selected_target.name}")
            self._set_preview(self.selected_target)

    def _set_preview(self, path: Path) -> None:
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            self.preview.setText("Preview unavailable")
            return
        self.preview.setPixmap(
            pixmap.scaled(
                self.preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.selected_target is not None:
            self._set_preview(self.selected_target)

    def _generate(self) -> None:
        source = self.source_box.currentData()
        if source is None or self.selected_target is None:
            self._show_error("Choose both a source collection and a target image first.")
            return
        self.generate_button.setEnabled(False)
        self.status_label.setText("Generating mosaic...")
        QApplication.processEvents()
        try:
            result = mosaic.generate(
                self.selected_target,
                self.rows_box.value(),
                self.columns_box.value(),
                Path(source),
            )
        except (FileNotFoundError, ValueError, OSError) as error:
            self._show_error(str(error))
            return
        finally:
            self.generate_button.setEnabled(True)
        self._set_preview(result)
        self.status_label.setText(f"Saved result to {result.name}")

    def _view_result(self) -> None:
        result = mosaic.DEFAULT_OUTPUT
        if not result.is_file():
            self._show_error("Generate a mosaic before opening the result.")
            return
        if not QPixmap(str(result)).isNull():
            self._set_preview(result)
        try:
            with Image.open(result) as image:
                image.show()
        except OSError as error:
            self._show_error(f"Could not open the result: {error}")

    def _show_error(self, message: str) -> None:
        self.status_label.setText(message)
        QMessageBox.warning(self, "Mosaic Generator", message)


def main() -> int:
    app = QApplication(sys.argv)
    window = MosaicInterface()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
