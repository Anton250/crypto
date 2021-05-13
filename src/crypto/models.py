from django.db import models
import json

class Algorythm(models.Model):
    TYPE_CIPHER = 'C'
    TYPE_SIGNATURE = 'S'
    TYPE_KEY_CHANGE = 'K'

    TYPES = [
        (TYPE_CIPHER, 'Шифр'),
        (TYPE_SIGNATURE, 'Цифровая подпись'),
        (TYPE_KEY_CHANGE, 'Обмен ключами'),
    ]

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64)
    class_name = models.CharField(max_length=128)
    key_opts = models.TextField(default='[]')
    no_alphabet = models.BooleanField(default=False)
    algo_num = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default=TYPE_CIPHER)

    @property
    def options(self):
        return json.loads(self.key_opts)

    def __str__(self):
        return self.name

class Alphabet(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.name
