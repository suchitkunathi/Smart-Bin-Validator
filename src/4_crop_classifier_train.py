import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras import layers, models

DATA_DIR = "data/crop_labeled"
BATCH = 16

datagen = ImageDataGenerator(
    rescale=1/255.0,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(224, 224),
    batch_size=BATCH,
    subset="training"
)

val_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(224, 224),
    batch_size=BATCH,
    subset="validation"
)

base = EfficientNetB3(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

model = models.Sequential([
    base,
    layers.GlobalAveragePooling2D(),
    layers.Dense(len(train_gen.class_indices), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(train_gen, validation_data=val_gen, epochs=10)

model.save("asin_classifier.keras")
print("✅ Saved classifier")
