import requests
from PIL import Image
import hashlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# 2.8.1 리퀘스트로 인터넷에서 이미지 파일 가져오기
url = 'http://bit.ly/2JnsHnT'
r = requests.get(url, stream=True).raw

src_img = '../../img/tmp/src.png'
dst_img = '../../img/tmp/dst.png'

# 2.8.2 필로우로 이미지 보여주기
img = Image.open(r)
print("img : ", img.get_format_mimetype)
# img.show()
img.save(src_img)

# 2.8.3 'with ~ as 파일 객체:'로 이미지 파일 복사
BUF_SIZE = 1024
with open(src_img, 'rb') as sf, open(dst_img, 'wb') as df:
    while True:
        data = sf.read(BUF_SIZE)
        if not data:
            break
        df.write(data)

# 2.8.4 SHA-256으로 파일 복사 검증하기
sha_src = hashlib.sha256()
sha_dst = hashlib.sha256()

with open(src_img, 'rb') as sf, open(dst_img, 'rb') as df:
    sha_src.update(sf.read())
    sha_dst.update(df.read())

print("src.png's hash : {}".format(sha_src.hexdigest()))
print("dsc.png's hash : {}".format(sha_dst.hexdigest()))

# 2.8.5 맷플롯립으로 이미지 가공하기
plt.suptitle('Image Processing', fontsize=18)
plt.subplot(1, 2, 1) # 1행 2열의 영역에서 첫 번째 영역으로 지정
plt.title('Original Image')
origin_img = mpimg.imread(src_img)
plt.imshow(origin_img) # 원본 파일을 읽어서 이미지로 표시
print(f'origin shape : {np.array(origin_img).shape}')

plt.subplot(122) # 1행 2열의 영역에서 두 번째 영역으로 지정
plt.title('Pseudocolor Image')
dst_img = mpimg.imread(dst_img)
pseudo_img = dst_img[:, :, 2]  # 의사 색상 적용
print(f'pseudo shape : {np.array(pseudo_img).shape}')
plt.imshow(pseudo_img)
plt.show()