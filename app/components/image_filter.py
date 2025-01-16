import cv2
from ultralytics import YOLO

FILTER_LIST = ['gray', 'object_detection']

class ImageFilter:
    def __init__(self, image=None):
        self.image = image
        self.filtered_image = None
        self.model = YOLO("../../models/yolov8n.pt")  # Pretrained YOLO model
        self.filter_type: str = 'gray'

    def set_filter_type(self, filter_type):
        self.filter_type = filter_type

    def update_filtered_image(self, image):
        self.image = image
        self.filtered_image = self.image.copy()

        if self.filter_type == 'gray':
            self.filtered_image = self.gray_filter()
        elif self.filter_type == 'object_detection':
            self.filtered_image = self.object_detection_filter()
        elif self.filter_type == 'detect_edges':
            self.filtered_image = self.detect_edges()

        return self.filtered_image

    def gray_filter(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel BGR
        self.filtered_image = gray_bgr
        return self.filtered_image


    def object_detection_filter(self):
        result = self.model(self.image, verbose=False)[0]
        self.filtered_image = self.image.copy()

        # Assuming result is the output from the YOLO model
        # Extract boxes, classes, and confidence scores
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding box coordinates [x1, y1, x2, y2]
        classes = result.boxes.cls.cpu().numpy().astype(int)  # Class indices
        confidences = result.boxes.conf.cpu().numpy()  # Confidence scores

        # Draw bounding boxes
        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i]  # Get coordinates
            class_id = classes[i]  # Get class ID
            confidence = confidences[i]  # Get confidence score

            label = f"{result.names[class_id]}: {confidence:.2f}"  # Class label and confidence
            color = (0, 255, 0)  # Green color for bounding box

            # Draw bounding box and label
            cv2.rectangle(self.filtered_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)  # Bounding box
            cv2.putText(self.filtered_image, label, (int(x1) + 5, int(y2) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # Label

        return self.filtered_image

    def detect_edges(self):
        print('Detecting edges')
        # current_image = self.image.copy()
        #
        # # Convert to grayscale
        # gray_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        #
        # # Perform Canny Edge Detection
        # self.filtered_image = cv2.Canny(gray_image, threshold1=0, threshold2=150)
        #
        return self.image