from header import *

class Pose_detection():
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        # Assign user's shoulder as limit of line that detect for jump and down
        self.shoudler_line_y = 0 
        self.threshold = 150

    def detectPose(self, image):
        # RGB color convert
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Take the output result
        results = self.pose.process(imageRGB)
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, landmark_list=results.pose_landmarks,
                                           connections=self.mp_pose.POSE_CONNECTIONS,
                                           landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 225, 255), thickness=3, circle_radius=3),
                                           connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))
        return image, results

    # Check the current position of object with Left, Right and Center
    def checkPose_LRC(self, image, results):
        # Assign input shape of image
        image_height, image_width, _ = image.shape
        image_mid_width = image_width // 2

        # Calculate the coordination of player shoulder, due to because the mp_pose only return % distance with middle image
        leftShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
        rightShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width)

        # Assign the result
        if (leftShoulder_x < image_mid_width) and (rightShoulder_x < image_mid_width): LRC = "L"
        elif (leftShoulder_x > image_mid_width) and (rightShoulder_x > image_mid_width): LRC = "R"
        else: LRC = "C"

        cv2.putText(image, LRC, (5, image_height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(image, (image_mid_width, 0), (image_mid_width, image_height), (255, 255, 255), 2)

        return image, LRC
    
    def checkHand_LRC(self, image, results):
        # Assign input shape of image
        image_height, image_width, _ = image.shape
        image_mid_width = image_width // 2

        # Calculate the coordination of player shoulder, due to because the mp_pose only return % distance with middle image
        leftHand_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * image_width)
        rightHand_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width)

        threshold = self.threshold+50

        # Assign the result
        if (leftHand_x < image_mid_width-threshold): LRC = "L"
        elif (leftHand_x > image_mid_width+threshold): LRC = "R"
        else: LRC = "C"

        cv2.putText(image, f"{LRC} with {leftHand_x}", (5, image_height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(image, (image_mid_width, 0), (image_mid_width, image_height), (255, 255, 255), 2)
        cv2.line(image, (image_mid_width+threshold, 0), (image_mid_width+threshold, image_height), (255, 255, 255), 2)
        cv2.line(image, (image_mid_width-threshold, 0), (image_mid_width-threshold, image_height), (255, 255, 255), 2)

        return image, LRC
    
    def checkHand_JSD(self, image, results):
        image_height, image_width, _ = image.shape
        image_mid_height = (image_height // 2) + 100

        leftHand_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)
        rightHand_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height)

        # centerShoulder_y = abs(leftShoulder_y + rightShoulder_y) // 2

        # Assign threshold for limitation of jump and down detection
        threshold = self.threshold

        # Assign the result
        if (leftHand_y < image_mid_height - threshold): JSD = "J"
        elif (leftHand_y > image_mid_height + threshold): JSD = "D"
        else: JSD = "S"

        cv2.putText(image, f"{JSD} with {leftHand_y} vs {image_mid_height}", (5, image_height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.line(image, (0, image_mid_height), (image_width, image_mid_height), (0, 255, 255), 2)
        cv2.line(image, (0, image_mid_height+threshold), (image_width, image_mid_height+threshold), (155, 155 , 255), 2)
        cv2.line(image, (0, image_mid_height-threshold), (image_width, image_mid_height-threshold), (255, 255, 255), 2)

        return image, JSD

    # Check the current action of object with Jump, Stay and Down
    def checkPose_JSD(self, image, results):
        image_height, image_width, _ = image.shape

        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
        rightShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)
        centerShoulder_y = abs(leftShoulder_y + rightShoulder_y) // 2

        # Assign threshold for limitation of jump and down detection
        jump_threshold = 50
        down_threshold = 50

        # Assign the result
        if (centerShoulder_y < self.shoudler_line_y - jump_threshold): JSD = "J"
        elif (centerShoulder_y > self.shoudler_line_y + down_threshold): JSD = "D"
        else: JSD = "S"

        cv2.putText(image, JSD, (5, image_height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.line(image, (0, self.shoudler_line_y), (image_width, self.shoudler_line_y), (0, 255, 255), 2)

        return image, JSD
    

    # Check user is clapping or not
    def checkPose_Clap(self, image, results):
        image_height, image_width, _ = image.shape

        left_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,
                     results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)

        right_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,
                      results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height)

        distance = int(math.hypot(left_hand[0] - right_hand[0], left_hand[1] - right_hand[1]))

        # Assign threshold for limitation of clap detection
        clap_threshold = 200

        if distance < clap_threshold: CLAP = "C"
        else: CLAP = "N"

        cv2.putText(image, f"{CLAP} with {distance}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)

        return image, CLAP
    

    # Storing user's shoulder limit line after clapping
    def save_shoulder_line_y(self, image, results):
        image_height, image_width, _ = image.shape

        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
        rightShoulder_y = int(
            results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)

        self.shoudler_line_y = abs(leftShoulder_y + rightShoulder_y) // 2
        return
