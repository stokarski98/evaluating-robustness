import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from transformers import TFBertModel, TFBertTokenizer, logging
logging.set_verbosity_error()

# Custom Keras layer for tokenizing input text using BERT tokenizer
class BertTokenizerLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = TFBertTokenizer.from_pretrained("bert-base-uncased")

    def call(self, inputs):
        tokens = self.tokenizer(
                inputs,
                padding="max_length",
                truncation=True,
                max_length=512
            )

        return tokens["input_ids"], tokens["attention_mask"], tokens["token_type_ids"]

#Function to build MalBERT, a BERT-based classification model
def build_MalBERT(model_weights_path: str | None = None):
    input_text = tf.keras.layers.Input(shape=(), dtype=tf.string, name="text_input")

    #Tokenizer layer
    tokenizer_layer = BertTokenizerLayer()
    input_ids, attention_mask, token_type_ids = tokenizer_layer(input_text)

    #Load pre-trained BERT model
    bert_model = TFBertModel.from_pretrained("bert-base-uncased")
    bert_outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
    pooled_output = bert_outputs.pooler_output

    #Classification layer
    net = tf.keras.layers.Dropout(0.1)(pooled_output)
    net = tf.keras.layers.Dense(512, activation='relu', name='classifier512')(net)
    net = tf.keras.layers.Dense(128, activation='relu', name='classifier128')(net)
    final_output = tf.keras.layers.Dense(2, activation='softmax', name='classifier2')(net)

    #
    model = tf.keras.Model(inputs=input_text, outputs=final_output)

    if model_weights_path is not None:
        model.load_weights(model_weights_path) 
    return model