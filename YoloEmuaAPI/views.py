from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageUpload, Detections
from .serializers import ImageUploadSerializer
from .detection_models.yolov8 import YOLOv8Detector 
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import os

def index(request):
    return render(request, 'index.html')

# def results(request):
#     print(request.FILES.get('fileup'))# 上传的图片文件
#     print(request.POST.get('confidence'))# 置信度
#     if request.method == 'POST' and request.FILES['fileup']:
#         myfile = request.FILES['fileup']
#         detector = YOLOv8Detector("/home/wl/MODELS/ultralytics-main/pt/yolov8n.pt")



#     # return render(request, 'results.html')
#     return HttpResponse("could not upload")

class UploadImageView_emua(APIView):
    detector = YOLOv8Detector("path/to/yolo.pt")

    def post(self, request, format=None):
        confidence_threshold = float(request.data.get('confidence_threshold', 0.5))

        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_upload = serializer.save()
            image_path = image_upload.image_file.path

            try:
                detection_result = self.detector.run_detection(
                    image_path=image_path,
                    confidence_threshold=confidence_threshold
                )

                image = cv2.imread(image_path)

                # 绘制检测框
                for detection in detection_result:
                    x_min, y_min = int(detection['x_min']), int(detection['y_min'])
                    x_max, y_max = int(detection['x_max']), int(detection['y_max'])
                    label = detection['label']
                    confidence = detection['confidence']

                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    cv2.putText(image, f"{label} {confidence:.2f}", (x_min, y_min - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # 保存每个检测结果到数据库
                    Detections.objects.create(
                        object_detection=image_upload,
                        label=label,
                        confidence=confidence,
                        x_min=x_min,
                        x_max=x_max,
                        y_min=y_min,
                        y_max=y_max
                    )

                output_image_path = image_path.replace('.jpg', '_detected.jpg')
                cv2.imwrite(output_image_path, image)

                image_upload.status = ImageUpload.STATUS_COMPLETED
                image_upload.save()

            except Exception as e:
                image_upload.status = ImageUpload.STATUS_FAILED
                image_upload.save()
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            relative_image_path = os.path.basename(output_image_path)
            print(detection_result)
            return render(request, 'results.html', {
                'outImg': relative_image_path,
                'detectionOut': {d['label']: d['confidence'] for d in detection_result}
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
