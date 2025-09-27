# Face Recognition Attendance System

This project is a **real-time face recognition-based attendance system** built with Python, OpenCV, and the `face_recognition` library.
It uses a webcam to detect and recognize students’ faces and automatically logs their attendance into a CSV file.

---

## Features

* Loads student images from a `students/` folder
* Detects and recognizes faces in real-time using a webcam
* Marks attendance (name + timestamp) in a daily CSV file
* Prevents duplicate entries for the same student
* Displays live video feed with bounding boxes and names

---

## Requirements

Make sure you have Python 3.7+ installed.
Install the required libraries:

```bash
pip install opencv-python face_recognition numpy
```

You also need to install **dlib** (required by `face_recognition`):

* On Ubuntu/Debian:

  ```bash
  sudo apt-get install cmake
  pip install dlib
  ```
* On Windows: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) first, then:

  ```bash
  pip install dlib
  ```

---

## Project Structure

```
face-attendance-system/
│
├── students/                # Folder containing student images
│   ├── john_doe.jpg
│   ├── jane_smith.png
│   └── ...
│
├── attendance_system.py     # Main Python script
├── README.md                # Project documentation
```

---

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/face-attendance-system.git
   cd face-attendance-system
   ```

2. Place student images in the `students/` folder.

   * Image names will be used as student names (e.g., `john_doe.jpg` → "John Doe").

3. Run the program:

   ```bash
   python attendance_system.py
   ```

4. Press **`q`** to quit the webcam feed.

5. Check the generated CSV file in the project directory:

   ```
   YYYY-MM-DD_attendance.csv
   ```

---

## Example Output

```
Name,Timestamp
John Doe,09:15:22
Jane Smith,09:18:45
```

---

## License

This project is open-source and available under the MIT License.
