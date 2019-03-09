import random

slope = []
another = []
actions = []

slope_roll = {
    "roll": ['right', 'left'],
    "yaw": ['right', 'left']
}
mouth_and_eyes = {
    "mouth": [],
    "eyes": ["right", "left"]
}
number = random.randint(3,4)
for i in range(number):
    if len(slope) < 2:
        roll_or_yaw = random.randint(0, 1)
        info_about_key = list(slope_roll.keys())[roll_or_yaw]
        right_or_left = random.randint(0, 1)
        info_about_argument = slope_roll[info_about_key][right_or_left]
        slope.append(info_about_key + '_' + info_about_argument)
    else:
        mouth_or_eyes = random.randint(0, 1)
        info_about_key = list(mouth_and_eyes.keys())[mouth_or_eyes]
        if info_about_key == 'eyes':
            right_or_left = random.randint(0, 1)
            info_about_argument = mouth_and_eyes[info_about_key][right_or_left]
            another.append(info_about_key + '_' + info_about_argument + '_close')
        else:
            info_about_argument = 'close'
            another.append(info_about_key + '_' + info_about_argument)
for i in slope:
    actions.append(i)
for i in another:
    actions.append(i)
print(actions)