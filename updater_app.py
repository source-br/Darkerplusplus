import sys
import os
import argparse
import time
import subprocess
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor


class UpdateRunnerWorker(QThread):
    """Background worker that handles process termination, silent installation, and app relaunch."""

    status_changed = Signal(str)
    progress_changed = Signal(int)
    finished_success = Signal()
    finished_error = Signal(str)

    def __init__(self, pid: int, installer_path: str, version: str, exe_path: str):
        super().__init__()
        self.pid = pid
        self.installer_path = installer_path
        self.version = version
        self.exe_path = exe_path

    def run(self):
        try:
            # Step 1: Wait for parent process to exit
            self.status_changed.emit("Encerrando Hammerfy...")
            self.progress_changed.emit(20)

            if self.pid > 0:
                self._wait_for_pid(self.pid)

            time.sleep(1.0)

            # Step 2: Launch installer silently
            self.status_changed.emit("Instalando arquivos da atualização...")
            self.progress_changed.emit(50)

            installer = Path(self.installer_path)
            if not installer.exists():
                self.finished_error.emit("Arquivo do instalador não encontrado.")
                return

            # Purge PyInstaller environment variables
            env = os.environ.copy()
            env.pop("_MEIPASS", None)
            env.pop("_MEIPASS2", None)

            cmd = [str(installer), "/SILENT", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"]
            proc = subprocess.Popen(cmd, env=env)
            proc.wait()

            self.progress_changed.emit(85)
            self.status_changed.emit("Reiniciando o Hammerfy...")
            time.sleep(1.0)

            # Step 3: Relaunch Hammerfy.exe
            exe = Path(self.exe_path)
            if exe.exists():
                subprocess.Popen([str(exe)], env=env)
            else:
                # Try finding in parent directory if relative
                default_exe = Path(__file__).parent / "Hammerfy.exe"
                if default_exe.exists():
                    subprocess.Popen([str(default_exe)], env=env)

            # Cleanup installer file
            try:
                if installer.exists():
                    installer.unlink()
            except Exception:
                pass

            self.progress_changed.emit(100)
            self.finished_success.emit()

        except Exception as e:
            self.finished_error.emit(str(e))

    def _wait_for_pid(self, pid: int):
        """Waits up to 5 seconds for PID to close cleanly."""
        start = time.time()
        while time.time() - start < 5.0:
            if not self._is_pid_running(pid):
                return
            time.sleep(0.3)

        # Force terminate if still running
        if self._is_pid_running(pid):
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)


    def _is_pid_running(self, pid: int) -> bool:
        if pid <= 0:
            return False
        if sys.platform == "win32":
            output = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True
            ).stdout
            return str(pid) in output
        else:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False


class UpdaterWindow(QWidget):
    """Modern dark/purple update window."""

    def __init__(self, pid: int, installer_path: str, version: str, exe_path: str):
        super().__init__()
        self.pid = pid
        self.installer_path = installer_path
        self.version = version
        self.exe_path = exe_path

        ver_str = version if version.startswith("v") or version.startswith("V") else f"v{version}"
        self.setWindowTitle(f"Hammerfy {ver_str} — Atualizando")
        self.setFixedSize(420, 180)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self._build_ui()
        self._apply_styles()
        self._start_update()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        ver_str = self.version if self.version.startswith("v") or self.version.startswith("V") else f"v{self.version}"

        self.title_lbl = QLabel(f"Instalando atualização {ver_str}")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #ffffff;")

        self.status_lbl = QLabel("Iniciando assistente de atualização...")
        self.status_lbl.setStyleSheet("font-size: 12px; color: #888888;")

        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(8)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(10)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("""
            QProgressBar {
                background-color: #22222b;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #7c6be0;
                border-radius: 4px;
            }
        """)

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.status_lbl)
        layout.addWidget(self.pbar)
        layout.addStretch()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #141418;
            }
        """)

    def _start_update(self):
        self.worker = UpdateRunnerWorker(self.pid, self.installer_path, self.version, self.exe_path)
        self.worker.status_changed.connect(self.status_lbl.setText)
        self.worker.progress_changed.connect(self.pbar.setValue)
        self.worker.finished_success.connect(QApplication.quit)
        self.worker.finished_error.connect(self._on_error)
        self.worker.start()

    def _on_error(self, err_msg: str):
        self.status_lbl.setText(f"Erro na atualização: {err_msg}")
        self.status_lbl.setStyleSheet("font-size: 12px; color: #e84a4a;")
        time.sleep(3)
        QApplication.quit()


def main():
    parser = argparse.ArgumentParser(description="Hammerfy Updater Companion")
    parser.add_argument("--pid", type=int, default=0, help="PID of Hammerfy process to wait for")
    parser.add_argument("--installer", type=str, required=True, help="Path to downloaded Setup.exe")
    parser.add_argument("--version", type=str, default="", help="Version string being installed")
    parser.add_argument("--exe", type=str, default="", help="Path to Hammerfy.exe to relaunch")

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = UpdaterWindow(args.pid, args.installer, args.version, args.exe)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
