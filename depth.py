import torch

from depth_anything_v2.dpt import DepthAnythingV2


# model = DepthAnythingV2(encoder='vitl', features=256, out_channels=[256, 512, 1024, 1024])
# model.load_state_dict(torch.load('checkpoints/depth_anything_v2_vitl.pth', map_location='cpu'))
# model.eval()

print("Loading Model")

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

encoder = 'vitl' # or 'vits', 'vitb', 'vitg'

model = DepthAnythingV2(**model_configs[encoder])
model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu', weights_only=False))
model = model.to(DEVICE).eval()

print("Model Loaded")


"""
Input -> 3d numpy array
Output -> 2d numpy array
"""
def createDepthMap(raw_img):
    depth_map = model.infer_image(raw_img) # HxW raw depth map
    depth_map_img = (depth_map / depth_map.max() * 255).astype('uint8')

    return depth_map_img


# if __name__ == "__main__":
#     pil_img = Image.open("assets/examples/demo03.jpg")
#     cv2_img = cv2.imread("assets/examples/demo03.jpg")
#     img_array = np.array(pil_img)
#     cv2.imwrite("exmapleout.jpg", createDepthMap(cv2_img))