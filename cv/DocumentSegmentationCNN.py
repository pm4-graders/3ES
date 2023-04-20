import os
import gc
import cv2
import numpy as np

import torch
import torchvision.transforms as torchvision_T
from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large


class DocumentSegmentationCNN:
    model = None
    
    def __init__(self):

        self.model = self.load_model()

    def load_model(self, num_classes=2, device=torch.device("cpu")):
        
        #Load pretrained model from file
        self.model = deeplabv3_mobilenet_v3_large(num_classes=num_classes, aux_loss=True)
        checkpoint_path = os.path.join(os.getcwd(), "cv/Models/model_mbv3_iou_mix_2C049.pth")

        self.model.to(device)
        checkpoints = torch.load(checkpoint_path, map_location=device)
        self.model.load_state_dict(checkpoints, strict=False)
        self.model.eval()

        _ = self.model(torch.randn((1, 3, 384, 384)))

        return self.model

    def image_preprocess_transforms(self, mean=(0.4611, 0.4359, 0.3905), std=(0.2193, 0.2150, 0.2109)):
        common_transforms = torchvision_T.Compose(
            [
                torchvision_T.ToTensor(),
                torchvision_T.Normalize(mean, std),
            ]
        )
        return common_transforms

    @staticmethod
    def order_points(pts):
        """Rearrange coordinates to order:
        top-left, top-right, bottom-right, bottom-left"""
        rect = np.zeros((4, 2), dtype="float32")
        pts = np.array(pts)
        s = pts.sum(axis=1)
        # Top-left point will have the smallest sum.
        rect[0] = pts[np.argmin(s)]
        # Bottom-right point will have the largest sum.
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        # Top-right point will have the smallest difference.
        rect[1] = pts[np.argmin(diff)]
        # Bottom-left will have the largest difference.
        rect[3] = pts[np.argmax(diff)]
        # return the ordered coordinates
        return rect.astype("int").tolist()

    def find_dest(self, pts):
        (tl, tr, br, bl) = pts
        # Finding the maximum width.
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Finding the maximum height.
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # Final destination co-ordinates.
        destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]

        return self.order_points(destination_corners)


    def align_document(self, image_true=None):
        
        #image = cv2.imdecode(file_bytes, 1)
        
        trained_model = self.model
        image_size = 384
        BUFFER = 10
        IMAGE_SIZE = image_size
        half = IMAGE_SIZE // 2
        
        h, w = image_true.shape[:2]

        imH, imW, C = image_true.shape

        image_model = cv2.resize(image_true, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_NEAREST)

        scale_x = imW / IMAGE_SIZE
        scale_y = imH / IMAGE_SIZE

        preprocess_transforms = self.image_preprocess_transforms()
        image_model = preprocess_transforms(image_model)
        image_model = torch.unsqueeze(image_model, dim=0)

        with torch.no_grad():
            out = trained_model(image_model)["out"].cpu()

        del image_model
        gc.collect()

        out = torch.argmax(out, dim=1, keepdims=True).permute(0, 2, 3, 1)[0].numpy().squeeze().astype(np.int32)
        r_H, r_W = out.shape

        _out_extended = np.zeros((IMAGE_SIZE + r_H, IMAGE_SIZE + r_W), dtype=out.dtype)
        _out_extended[half : half + IMAGE_SIZE, half : half + IMAGE_SIZE] = out * 255
        out = _out_extended.copy()

        del _out_extended
        gc.collect()

        # Edge Detection.
        canny = cv2.Canny(out.astype(np.uint8), 225, 255)
        canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        page = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        # ==========================================
        epsilon = 0.02 * cv2.arcLength(page, True)
        corners = cv2.approxPolyDP(page, epsilon, True)

        corners = np.concatenate(corners).astype(np.float32)

        corners[:, 0] -= half
        corners[:, 1] -= half

        corners[:, 0] *= scale_x
        corners[:, 1] *= scale_y

        # check if corners are inside.
        # if not find smallest enclosing box, expand_image then extract document
        # else extract document

        if not (np.all(corners.min(axis=0) >= (0, 0)) and np.all(corners.max(axis=0) <= (imW, imH))):

            left_pad, top_pad, right_pad, bottom_pad = 0, 0, 0, 0

            rect = cv2.minAreaRect(corners.reshape((-1, 1, 2)))
            box = cv2.boxPoints(rect)
            box_corners = np.int32(box)
            #     box_corners = minimum_bounding_rectangle(corners)

            box_x_min = np.min(box_corners[:, 0])
            box_x_max = np.max(box_corners[:, 0])
            box_y_min = np.min(box_corners[:, 1])
            box_y_max = np.max(box_corners[:, 1])

            # Find corner point which doesn't satify the image constraint
            # and record the amount of shift required to make the box
            # corner satisfy the constraint
            if box_x_min <= 0:
                left_pad = abs(box_x_min) + BUFFER

            if box_x_max >= imW:
                right_pad = (box_x_max - imW) + BUFFER

            if box_y_min <= 0:
                top_pad = abs(box_y_min) + BUFFER

            if box_y_max >= imH:
                bottom_pad = (box_y_max - imH) + BUFFER

            # new image with additional zeros pixels
            image_extended = np.zeros((top_pad + bottom_pad + imH, left_pad + right_pad + imW, C), dtype=image_true.dtype)

            # adjust original image within the new 'image_extended'
            image_extended[top_pad : top_pad + imH, left_pad : left_pad + imW, :] = image_true
            image_extended = image_extended.astype(np.float32)

            # shifting 'box_corners' the required amount
            box_corners[:, 0] += left_pad
            box_corners[:, 1] += top_pad

            corners = box_corners
            image_true = image_extended

        corners = sorted(corners.tolist())
        corners = self.order_points(corners)
        destination_corners = self.find_dest(corners)
        M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))

        final = cv2.warpPerspective(image_true, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LANCZOS4)
        final = np.clip(final, a_min=0, a_max=255)
        final = final.astype(np.uint8)

        return final
