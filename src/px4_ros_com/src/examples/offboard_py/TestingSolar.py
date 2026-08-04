import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

import cv2
import numpy as np
from ultralytics import YOLO

# --- init GStreamer ---
Gst.init(None)

PIPELINE = (
    'udpsrc port=5601 '
    'caps="application/x-rtp, media=video, clock-rate=90000, '
    'encoding-name=H264, payload=96" ! '
    'rtph264depay ! avdec_h264 ! videoconvert ! '
    'video/x-raw,format=BGR ! appsink name=sink sync=false'
)

pipeline = Gst.parse_launch(PIPELINE)
appsink = pipeline.get_by_name("sink")

appsink.set_property("emit-signals", True)
appsink.set_property("max-buffers", 1)
appsink.set_property("drop", True)

pipeline.set_state(Gst.State.PLAYING)

print("Stream GStreamer ok")

# --- load YOLO ---
model = YOLO("yolov8n.pt")  # nano = rapid

print("YOLO ok")

# --- main loop ---
while True:
    sample = appsink.emit("pull-sample")
    if sample is None:
        continue

    buf = sample.get_buffer()
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value("width")
    height = caps.get_structure(0).get_value("height")

    success, mapinfo = buf.map(Gst.MapFlags.READ)
    if not success:
        continue

    frame = np.frombuffer(mapinfo.data, dtype=np.uint8)
    frame = frame.reshape((height, width, 3)).copy()
    buf.unmap(mapinfo)

    # --- YOLO inference ---
    results = model(frame, verbose=False)

    # --- draw detections ---
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame, label, (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

    cv2.imshow("YOLO PX4 Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipeline.set_state(Gst.State.NULL)
cv2.destroyAllWindows()
