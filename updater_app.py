import sys
import os
import argparse
import time
import shutil
import zipfile
import subprocess
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal


class UpdateRunnerWorker(QThread):
    """Background worker that handles process termination, zip extraction / silent installation, and app relaunch."""

    status_changed = Signal(str)
    progress_changed = Signal(int)
    finished_success = Signal()
    finished_error = Signal(str)

    def __init__(self, pid: int, zip_path: str, installer_path: str, target_dir: str, version: str, exe_path: str):
        super().__init__()
        self.pid = pid
        self.zip_path = zip_path
        self.installer_path = installer_path
        self.target_dir = target_dir
        self.version = version
        self.exe_path = exe_path

    def run(self):
        try:
            # Step 1: Wait for parent Hammerfy process to exit
            self.status_changed.emit("Encerrando Hammerfy...")
            self.progress_changed.emit(15)

            if self.pid > 0:
                self._wait_for_pid(self.pid)

            time.sleep(0.5)

            env = os.environ.copy()
            env.pop("_MEIPASS", None)
            env.pop("_MEIPASS2", None)

            # Step 2: Handle ZIP extraction (Preferred Silent Mode)
            if self.zip_path and Path(self.zip_path).exists():
                self.status_changed.emit("Extraindo arquivos da atualização...")
                self.progress_changed.emit(40)

                target = Path(self.target_dir) if self.target_dir else Path(self.exe_path).parent
                target.mkdir(parents=True, exist_ok=True)

                zip_file = Path(self.zip_path)
                with zipfile.ZipFile(zip_file, 'r') as archive:
                    members = archive.infolist()
                    total_members = len(members)
                    for idx, member in enumerate(members):
                        archive.extract(member, target)
                        if total_members > 0:
                            pct = 40 + int((idx / total_members) * 45)
                            self.progress_changed.emit(pct)

                self.progress_changed.emit(85)
                self.status_changed.emit("Reiniciando o Hammerfy...")
                time.sleep(0.5)

                # Cleanup zip file
                try:
                    zip_file.unlink()
                except Exception:
                    pass

            # Step 2 Fallback: Handle EXE installer
            elif self.installer_path and Path(self.installer_path).exists():
                self.status_changed.emit("Instalando arquivos da atualização...")
                self.progress_changed.emit(50)

                installer = Path(self.installer_path)
                cmd = [str(installer), "/SILENT", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"]
                proc = subprocess.Popen(cmd, env=env)
                proc.wait()

                self.progress_changed.emit(85)
                self.status_changed.emit("Reiniciando o Hammerfy...")
                time.sleep(0.5)

                try:
                    installer.unlink()
                except Exception:
                    pass
            else:
                self.finished_error.emit("Pacote de atualização não encontrado.")
                return

            # Step 3: Relaunch Hammerfy.exe
            exe = Path(self.exe_path)
            if exe.exists():
                subprocess.Popen([str(exe)], env=env)
            else:
                target_exe = (Path(self.target_dir) / "Hammerfy.exe") if self.target_dir else None
                if target_exe and target_exe.exists():
                    subprocess.Popen([str(target_exe)], env=env)

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
            time.sleep(0.2)

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
    """Modern dark/purple update window matching Hammerfy color palette."""

    def __init__(self, pid: int, zip_path: str, installer_path: str, target_dir: str, version: str, exe_path: str):
        super().__init__()
        self.pid = pid
        self.zip_path = zip_path
        self.installer_path = installer_path
        self.target_dir = target_dir
        self.version = version
        self.exe_path = exe_path

        ver_str = version if version.startswith("v") or version.startswith("V") else f"v{version}"
        self.setWindowTitle(f"Hammerfy {ver_str} — Atualizando")
        self.setFixedSize(440, 175)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        # Set application icon
        icon_path = Path(__file__).parent / "assets" / "icons" / "hammerfy-icon.ico"
        if icon_path.exists():
            from PySide6.QtGui import QIcon
            self.setWindowIcon(QIcon(str(icon_path)))

        self._build_ui()
        self._apply_styles()
        self._start_update()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        ver_str = self.version if self.version.startswith("v") or self.version.startswith("V") else f"v{self.version}"

        # Header with Logo / Icon
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(22, 22)
        icon_path_png = Path(__file__).parent / "assets" / "icons" / "hammerfy-icon.png"
        if icon_path_png.exists():
            from PySide6.QtGui import QPixmap
            icon_lbl.setPixmap(QPixmap(str(icon_path_png)).scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.title_lbl = QLabel(f"Instalando atualização {ver_str}")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #f0f0f0; background: transparent;")

        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()

        self.status_lbl = QLabel("Iniciando assistente de atualização...")
        self.status_lbl.setStyleSheet("font-size: 12px; color: #888888; background: transparent;")

        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(8)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(10)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("""
            QProgressBar {
                background-color: #2a2a2a;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #7c6be0;
                border-radius: 4px;
            }
        """)

        layout.addLayout(header_layout)
        layout.addWidget(self.status_lbl)
        layout.addWidget(self.pbar)
        layout.addStretch()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
            }
        """)

    def _start_update(self):
        self.worker = UpdateRunnerWorker(
            self.pid, self.zip_path, self.installer_path, self.target_dir, self.version, self.exe_path
        )
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


def self_relaunch_from_temp_if_needed(target_dir: str):
    """If running as a frozen EXE inside target_dir, copy self to TEMP and relaunch so target files aren't locked."""
    if not getattr(sys, 'frozen', False):
        return

    current_exe = Path(sys.executable).resolve()
    temp_runner = Path(os.environ.get("TEMP", ".")) / "HammerfyUpdater_runner.exe"

    if current_exe != temp_runner.resolve():
        try:
            shutil.copy2(current_exe, temp_runner)
            cmd = [str(temp_runner)] + sys.argv[1:]
            subprocess.Popen(cmd)
            sys.exit(0)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Hammerfy Updater Companion")
    parser.add_argument("--pid", type=int, default=0, help="PID of Hammerfy process to wait for")
    parser.add_argument("--zip", type=str, default="", help="Path to downloaded update.zip")
    parser.add_argument("--installer", type=str, default="", help="Path to downloaded Setup.exe")
    parser.add_argument("--target", type=str, default="", help="Target installation directory")
    parser.add_argument("--version", type=str, default="", help="Version string being installed")
    parser.add_argument("--exe", type=str, default="", help="Path to Hammerfy.exe to relaunch")

    args = parser.parse_args()

    # Relaunch from TEMP if running inside the target directory to prevent self file-locking
    if args.target:
        self_relaunch_from_temp_if_needed(args.target)

    app = QApplication(sys.argv)
    window = UpdaterWindow(args.pid, args.zip, args.installer, args.target, args.version, args.exe)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
