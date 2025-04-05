import tensorflow as tf
import numpy as np
from PIL import Image
import io
from typing import List, Tuple, Dict

class ObjectRecognitionService:
    def __init__(self):
        # Cargar el modelo pre-entrenado (MobileNet V2)
        this.model = tf.keras.applications.MobileNetV2(weights='imagenet')
        # Cargar las clases de ImageNet
        this.class_names = tf.keras.applications.mobilenet_v2.decode_predictions

    def recognize_objects(self, image_data: bytes, confidence_threshold: float = 0.5) -> List[Dict[str, float]]:
        try:
            # Convertir bytes a imagen
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Redimensionar la imagen al tamaño requerido por MobileNetV2
            image = image.resize((224, 224))
            
            # Convertir a array y preprocesar
            image_array = np.array(image)
            image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
            image_array = np.expand_dims(image_array, axis=0)
            
            # Realizar la predicción
            predictions = this.model.predict(image_array)
            decoded_predictions = this.class_names(predictions)[0]
            
            # Filtrar predicciones por umbral de confianza
            results = []
            for _, label, confidence in decoded_predictions:
                if confidence >= confidence_threshold:
                    results.append({
                        "label": label,
                        "confidence": float(confidence)
                    })
            
            return results
        except Exception as e:
            print(f"Error al reconocer objetos: {str(e)}")
            return []

    def get_model_info(self) -> Dict[str, str]:
        return {
            "name": "MobileNetV2",
            "input_size": "224x224",
            "dataset": "ImageNet",
            "classes": "1000"
        } 