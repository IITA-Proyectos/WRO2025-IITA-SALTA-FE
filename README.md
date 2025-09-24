# 🤖 WRO 2025 – Future Engineers  
## Project: Autonomous Car – Team *IITA InnovaX*

---

## 📌 Project Description  
The **Future Engineers Challenge** of WRO 2025 invites teams to design, build, and program an autonomous car capable of completing a defined track, facing obstacles, and simulating the real challenges in the development of intelligent vehicles.  

Our goal as a team is to **create a robot that combines mechanical precision, reliable sensor integration, efficient software and Computer Vision**, ensuring stable performance on the track.  

The development process followed an **iterative engineering cycle**:  
1. **Ideate** → brainstorming and planning.  
2. **Build** → mechanical and electronic implementation.  
3. **Test** → validation on the track.  
4. **Evaluate** → analysis of results.  
5. **Improve** → feedback and optimization.  

All these stages are documented in the **Engineering Journal**, highlighting not only the final product but also the engineering journey.

---

## ⚙️ Mechanical Design  
The car was engineered with a strong emphasis on **stability, precision, and reliability**:  

- **Rear-wheel drive with mechanical differential** → the traction motor is connected to the rear axle through a differential, allowing the left and right wheels to rotate at different speeds when turning. This prevents wheel slip, reduces stress on the drivetrain, and mimics real car dynamics.  
- **Car-like steering system (Ackermann steering geometry)** with a dedicated front motor → provides smoother and more realistic turns than differential drive systems.  
- **Custom modular LEGO chassis** → designed for robustness and quick maintenance, enabling fast adjustments during testing sessions and competitions.  
- **Optimized weight distribution and low center of gravity** → strategic placement of motors, sensors, and hub reduces drift and improves stability in sharp turns.  
- **Scalable architecture** → chassis layout allows integration of additional sensors (e.g., OpenMV camera or LiDAR) without compromising balance or performance.  

This design provides the robot with **authentic vehicle behavior**, improving accuracy in navigation, efficiency in cornering, and overall track performance.    



## 🔬 Sensors & Electronics  
The following sensors were integrated for autonomous navigation:  
- **IMU** → heading control with proportional correction (KP)
- **Color sensor** → detection of floor colors  
- **Ultrasonic sensors** → navigation along the scenario
- **OpenMV Camera** -> Computer vision employed for obstacles recognition

---

## 💻 Software Development  
The software was developed in **Pybricks (MicroPython)**.  
Key features:  
- 🚗 **Straight driving control with IMU + KP** to correct deviations.  
- 🔄 **Color-based logic** to determine driving direction according to the rules.  
- 🧠 **Modular architecture** → robot class and utility functions split across files.  
- 📡 **Integration with OpenMV H7 Camera** → advanced object and signal detection.  

## 📂 Repository Structure  
```
├── docs/                        # Documentation and diagrams
│   ├── engineering_journal.pdf
│   └── WRO - Electrical Diagram.png
├── src/                         # Source code
│   ├── OpenChallengeCode/
│   │  ├── MainScript.py
│   │  └── robot_funcional93.py
│   ├── ObstacleChallengeCode/
│   │  └── Main_ObstacleChallenge.py
│   ├── Funciones.py             # Helper Functions (prototype)
│   ├── IITA_Motion.py           # Prototype
│   ├── BasicMovementFE.py       # Prototype
│   └── main.py                  # Prototype
├── Videos/
│      ├── WRO FE - Desafío Abierto.mp4
│      └── WRO Fe - Desafío de Obstáculos.mp4
└── README.md                    # This file
```


## 🚀 Using the Repository

1. Clone this repository:  

   ```bash
   git clone https://github.com/IITA-Proyectos/WRO2025-IITA-SALTA-FE
   cd WRO-2025-FutureEngineers
2. Search into src/OpenChallengeCode or src/ObstacleChallengeCode for script files and upload it into Spike Hub using PyBricks IDE
3. Connect motors and sensors according to (docs/hardware_setup.png)
4. Place the robot on the official WRO track scenario and power it on.

## 🏆 Rules & Compliance  
This project complies with the **WRO Future Engineers 2025 General Rules**, including:  
- Use of approved components.  
- Respecting weight and size limits.  
- Fully autonomous implementation (no remote control during runs).  
- Documentation provided in both Engineering Journal and GitHub README.

## 👥 Team Members  
- **Gerardo Benjamín Uriburu Romero** – Team Leader & Programmer
- **Natanahel Fernández** – Team sub-leader & Computing Vision Programmer
- **Enzo Juárez** - Mentor & Professor

## 📢 License  
This project is released under the **MIT License** – free to use and adapt for educational purposes.  

## ✨ Acknowledgements  
- Special thanks to **Instituto de Innovación y Tecnología Aplicada** for academic, logistical and financial support.
- **Mentors and Professors** who share their knowledge with us for the project 
- **Instituto de Innovación y Tecnología Aplicada Community** for their support
- **WRO community** for providing the framework for innovation and competition.
- **Our families and friends** for their moral support
