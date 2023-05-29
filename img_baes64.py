import json
import cv2
import io
from PIL import Image

# mask_img 为图像np.ndarray
result_dict = ()
img_encode = cv2.imencode('.png', mask_img[:,:,1])[1]
data_encode = base64.b64encode(img_encode)
data_str = data_encode.decode()
result_dict["mask"] = data_str

# json序列化，发送数据
result = json.dumps(return_dict, ensure_ascii=False)

# 接收数据，解码
mask_data = result["mask"]
mask_data = base64.b64decode(mask_data)
filejpgdata = io.BytesIO(mask_data)
mask_img = Image.open(filejpgdata).convert('L')
mask_img = np.asarray(mask_img)
cv2.imwrite("mask.png", mask_img)
