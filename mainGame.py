from header import *
from detectPose import Pose_detection

parser = argparse.ArgumentParser()
parser.add_argument('--playmode', default='Hand', help='Method of recognition for the game, including Body or Hand')
parser.add_argument('--anchorpoint', default='15', help='The point of user body that represent for landmark detection')
parser.add_argument('--threshold', default='150', help='The limitation of threshold for action an activity')
opt = parser.parse_args()

class SubwaySuffers():
    def __init__(self):
        self.pose = Pose_detection(opt.anchorpoint, opt.threshold)
        self.game_started = False
        self.x_position = 1 # position of player in game, 0 means left way, 1 center and 2 means right ways
        self.y_position = 1 # ction of player in game, 0 means down, 1 stay and 2 means jump
        self.clap_duration = 0 # set number of frame clapping
        self.playMode = opt.playmode
        self.delay = 0
        self.lstm = tf.keras.models.load_model("model.h5")
        self.n_time_steps = 10
        self.lm_list = []
        self.label_lstm = None
        self.thread = None

    def move_LRC(self, LRC):
        self.delay+=1
        if self.delay <= 30: return
        if LRC=="L" and self.x_position!=0:                     
            [pyautogui.press('left') for _ in range(self.x_position)]
            # pyautogui.press('left')
            # print('move to left')
            self.x_position = 0
        elif LRC=="R" and self.x_position!=2:
            [pyautogui.press('right') for _ in range(2, self.x_position, -1)]
            # pyautogui.press('right')
            # print('move to right')
            self.x_position = 2
        elif LRC=="C" and self.x_position!=1:
            if self.x_position==0:
                pyautogui.press('right')
                # print('move to center')
            elif self.x_position== 2:
                pyautogui.press('left')
                # print('move to center')
            self.x_position = 1

    def move_JSD(self, JSD): 
        if (JSD=="J") and (self.y_position == 1):
            pyautogui.press('up')
            # print('Jumping')
            self.y_position = 2
        elif (JSD=="D") and (self.y_position ==1):
            pyautogui.press('down')
            # print('Scrolling')
            self.y_position = 0
        elif (JSD=="S") and (self.y_position !=1):
            self.y_position = 1
        return
    
    def kill_thread(self):
        if self.thread is not None:
            self.thread = None
        self.label_lstm = []
        
    
    def make_landmark_timestep(self, results):
        c_lm = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            c_lm.append(lm.x)
            c_lm.append(lm.y)
            c_lm.append(lm.z)
            c_lm.append(lm.visibility)
        return c_lm
    

    def human_activity_detection(self, results):
        def detect(model, lm_list):
            lm_list = np.array(lm_list)
            lm_list = np.expand_dims(lm_list, axis=0)
            detection = model.predict(lm_list)
            if detection[0][0] > 0.5: self.label_lstm = "SWING BODY"
            else: self.label_lstm = "SWING HAND"
            print(self.label_lstm)

        c_lm = self.make_landmark_timestep(results)
        self.lm_list.append(c_lm)
        if len(self.lm_list) == self.n_time_steps:
            self.thread = threading.Thread(target=detect, args=(self.lstm, self.lm_list,))
            self.thread.start()
        
    def check_start_engine(self, image, results):
        if self.game_started:
            self.kill_thread()
            return
        self.human_activity_detection(results)
        image, CLAP = self.pose.checkPose_Clap(image, results)
        if CLAP == "C":
            self.clap_duration +=1
            if self.clap_duration == 10 and self.label_lstm is not None:
                self.game_started  = True
                self.pose.save_shoulder_line_y(image, results)
                pyautogui.click(x=720, y = 560, button = "left")
                self.clap_duration = 0
        else:
            self.clap_duration = 0

    def play(self):
        # Set constant size for video
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

        while True:
            ret, image = cap.read()
            if ret:
                image = cv2.flip(image, 1)
                image_height, image_width, _ = image.shape
                image, results = self.pose.detectPose(image)

                if results.pose_landmarks:
                    # check whether game started or not
                    if self.game_started:
                        image, LRC = self.pose.checkHand_LRC(image, results) if self.playMode=='Hand' else self.pose.checkPose_LRC(image, results)
                        self.move_LRC(LRC)

                        image, JSD = self.pose.checkHand_JSD(image, results) if self.playMode=='Hand' else self.pose.checkPose_JSD(image, results)
                        self.move_JSD(JSD)
                    else:
                        cv2.putText(image, "Clap your hand to start!", (5, image_height-10), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 3)

                    self.check_start_engine(image, results)

                cv2.imshow("Game", image)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

myGame = SubwaySuffers()
myGame.play()