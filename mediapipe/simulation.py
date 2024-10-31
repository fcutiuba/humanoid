import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtOpenGL import QOpenGLWidget
import pybullet as p
import pybullet_data

class BulletGLWidget(QOpenGLWidget):
    def initializeGL(self):
        # Initialize PyBullet in DIRECT mode to avoid an additional window
        p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.loadURDF("mock.urdf")
        self.robot_id = p.loadURDF("r2d2.urdf")
        p.setGravity(0, 0, -9.81)

    def paintGL(self):
        p.stepSimulation()
        # TODO: Render logic can be added here
        self.update() 

    def closeEvent(self, event):
        p.disconnect()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.glWidget = BulletGLWidget()
        self.setCentralWidget(self.glWidget)
        self.setWindowTitle("PyQt + PyBullet Integration")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
