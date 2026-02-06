import gc
import numpy as np
import pyaudio
from openwakeword.model import Model
import os


class VoiceEngine:
    __slots__ = ["model", "threshold", "gain", "pa", "is_running", "handlers", "stream"]

    def __init__(self, model_filename=None, wakewords=None, threshold=0.4, gain=2.0):
        model_path = None
        if model_filename:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, model_filename)

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model doesnt exists: {model_path}")

        self.model = Model(
            wakeword_models=wakewords,
            inference_framework="onnx",
        )

        self.threshold = threshold
        self.gain = gain
        self.pa = pyaudio.PyAudio()
        self.is_running = False
        self.handlers = {}
        self.stream = None

    def add_handler(self, keyword, func):
        self.handlers[keyword] = func

    def run(self):
        self.is_running = True

        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1280

        self.stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        gc.collect()

        try:
            while self.is_running:
                data = self.stream.read(CHUNK, exception_on_overflow=False)

                audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                if self.gain != 1.0:
                    audio_np *= self.gain

                prediction = self.model.predict(audio_np)

                for md, prob in prediction.items():
                    if prob > self.threshold:
                        if md in self.handlers:
                            self.handlers[md]()
                        self.model.reset()

        except Exception as e:
            pass
        finally:
            self.stop()

    def stop(self):
        self.is_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()
        gc.collect()
