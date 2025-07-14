https://github.com/user-attachments/assets/6f92c1f7-2816-493a-8ad7-a00f3f75cce8

Pentru a rula aplicația trebuie instalate următoarele aplicații:
 * Gazebo classic : https://docs.px4.io/main/en/sim_gazebo_classic/
 * ROS 2: https://docs.px4.io/main/en/ros2/user_guide.html

 * XRCE :	git clone -b v2.4.2 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git
		cd Micro-XRCE-DDS-Agent
		mkdir build
		cd build
		cmake ..
		make
		sudo make install
		sudo ldconfig /usr/local/lib/

Pentru rularea proiectului, după pull local se va rula urmatoarea secvență, pentru a deschide interfața prin linia de comanda:

	cd ~/ws_ros2
	source /opt/ros/humble/setup.bash
	colcon build
	source install/local_setup.bash
	source install/setup.bash
	ros2 run px4_ros_com Main.py

După rulare se va deschide un meniu:
Opțiuni meniu:

1. **Pornire Simulare** – Deschide Gazebo cu drona custom.
2. **Pornire Comunicație** – Pornește agentul UDP.
3. **Lansare Dronă** – Rulează nodul de control dronă (**armare, zbor, evitare**).
4. **Person Detection** – Pornește detecția de persoane.
5. **Cartography** – Trimite puncte și marchează traseul pe hartă.
