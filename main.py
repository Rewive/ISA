class ImageEncoderDecoder:
    def __init__(self, password):
        self.password = password.encode()

    def encode_image(self, img_path):
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import os
        import base64
        import json
        import numpy as np
        from PIL import Image, PngImagePlugin, ImageOps
        import random
        import gzip

        salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.password))

        img = Image.open(img_path).convert("RGBA")

        r, g, b, a = img.split()

        r = ImageOps.invert(r)
        g = ImageOps.invert(g)
        b = ImageOps.invert(b)

        img = Image.merge("RGBA", (r, g, b, a))
        pixels = np.array(img)

        strips = np.split(pixels, pixels.shape[0])

        horizontal_order = list(range(len(strips)))
        random.shuffle(horizontal_order)
        shuffled_strips = [strips[i] for i in horizontal_order]

        segmented_strips = [np.hsplit(strip, strip.shape[1]) for strip in shuffled_strips]

        segment_order = []
        for strip in segmented_strips:
            vertical_order = list(range(len(strip)))
            random.shuffle(vertical_order)
            segment_order.append(vertical_order)
            strip[:] = [strip[i] for i in vertical_order]

        recombined_strips = [np.concatenate(strip, axis=1) for strip in segmented_strips]

        new_img = Image.fromarray(np.concatenate(recombined_strips, axis=0))

        vertical_data = [list(map(int, order)) for order in segment_order]
        horizontal_data = list(map(int, horizontal_order))

        json_vertical_data = json.dumps(vertical_data)
        json_horizontal_data = json.dumps(horizontal_data)

        compressed_vertical_data = gzip.compress(json_vertical_data.encode())
        compressed_horizontal_data = gzip.compress(json_horizontal_data.encode())

        cipher_suite = Fernet(key)
        cipher_vertical_text = cipher_suite.encrypt(compressed_vertical_data)
        cipher_horizontal_text = cipher_suite.encrypt(compressed_horizontal_data)

        encrypted_all_data = {
            'integral': cipher_vertical_text.decode(),
            'difiriential': cipher_horizontal_text.decode(),
            'correct': base64.urlsafe_b64encode(salt).decode()
        }

        json_encrypted_all_data = json.dumps(encrypted_all_data)

        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("encrypted_data", json_encrypted_all_data)

        return {'image': new_img, 'metadata': metadata}

    def decode_image(self, shuffled_img_path):
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64
        import json
        import numpy as np
        from PIL import Image, ImageOps
        import gzip

        img = Image.open(shuffled_img_path).convert("RGBA")
        metadata = img.info
        json_encrypted_all_data = metadata.get("encrypted_data")

        encrypted_all_data = json.loads(json_encrypted_all_data)

        salt = base64.urlsafe_b64decode(encrypted_all_data['correct'])

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.password))

        cipher_suite = Fernet(key)

        cipher_vertical_text = cipher_suite.decrypt(encrypted_all_data['integral'].encode())
        cipher_horizontal_text = cipher_suite.decrypt(encrypted_all_data['difiriential'].encode())

        gzip_decompressed_vertical_data = gzip.decompress(cipher_vertical_text).decode()
        gzip_decompressed_horizontal_data = gzip.decompress(cipher_horizontal_text).decode()

        vertical_data = json.loads(gzip_decompressed_vertical_data)
        horizontal_data = json.loads(gzip_decompressed_horizontal_data)

        pixels = np.array(img)
        strips = np.split(pixels, pixels.shape[0])

        segmented_strips = [np.hsplit(strip, strip.shape[1]) for strip in strips]

        for i, strip in enumerate(segmented_strips):
            ordered_segments = [None]*len(strip)
            for j, segment in enumerate(strip):
                ordered_segments[vertical_data[i][j]] = segment
            strip[:] = ordered_segments

        recombined_strips = [np.concatenate(strip, axis=1) for strip in segmented_strips]

        ordered_strips = [None]*len(recombined_strips)
        for i, strip in enumerate(recombined_strips):
            ordered_strips[horizontal_data[i]] = strip

        new_img = Image.fromarray(np.concatenate(ordered_strips, axis=0))

        r, g, b, a = new_img.split()

        r = ImageOps.invert(r)
        g = ImageOps.invert(g)
        b = ImageOps.invert(b)

        new_img = Image.merge("RGBA", (r, g, b, a))

        return new_img