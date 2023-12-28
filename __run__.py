from main import ImageEncoderDecoder

def run():
    encoder_decoder = ImageEncoderDecoder('123')

    result = encoder_decoder.encode_image('input/go.jpg')
    result['image'].save('shuffled/shuffled.png', pnginfo=result['metadata'])

    original_img = encoder_decoder.decode_image('shuffled/shuffled.png')
    original_img.save('out/original.png')

if __name__ == "__main__":
    run()