import serial
import threading
import json


class SerialReader:
    def __init__(self, port="/dev/serial0", baudrate=115200, callback=None):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.ser.reset_input_buffer()
        self.callback = callback

        threading.Thread(target=self._read_loop, daemon=True).start()

    def _read_loop(self):
        while True:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()

                if not line:
                    continue

                # print("Raw line:", line)

                # 🔥 ambil JSON walaupun ada prefix
                if "{" in line and "}" in line:
                    json_str = line[line.find("{"):line.rfind("}") + 1]

                    try:
                        data = json.loads(json_str)

                        if self.callback:
                            self.callback(data)

                    except:
                        pass

            except Exception as e:
                print("Serial error:", e)

    def send(self, data: dict):
        try:
            json_data = json.dumps(data, separators=(',', ':')) + "\n"
            self.ser.write(json_data.encode("utf-8"))
        except Exception as e:
            print("Send error:", e)

    def send_raw(self, text: str):
        try:
            self.ser.write((text + "\n").encode("utf-8"))
        except Exception as e:
            print("Send error:", e)