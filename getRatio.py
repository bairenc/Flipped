#given an url of an image, use Facial Analysis to get ratios that describe facial features, put them in dictionary and output to server

def getRatios(imageUrl):
    import math
    import requests

    url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/landmarks"

    querystring = {"photo":imageUrl}

    payload = ""
    headers = {
        'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
        'x-rapidapi-key': "fb7926bb8emshd3f86e009645bcap1bc99bjsn075d7a07f2a1",
        'content-type': "application/x-www-form-urlencoded"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    #print(type(response))
    rinj = response.json()

    iBrow_y = rinj['landmarks'][0]['right_eyebrow']['middle']['y']
    iBrowRight_x = rinj['landmarks'][0]['right_eyebrow']['outer_corner']['x']
    iUpper_y = rinj['landmarks'][0]['right_eye']['upper_line2']['y']
    iLower_y = rinj['landmarks'][0]['right_eye']['lower_line2']['y']
    iCenter_y = rinj['landmarks'][0]['right_eye']['center']['y']
    iCenter_x = rinj['landmarks'][0]['right_eye']['center']['x']
    iRight_x = rinj['landmarks'][0]['right_eye']['outer_corner']['x']
    iLeft_x = rinj['landmarks'][0]['right_eye']['inner_corner']['x']
    noseUpper_y = rinj['landmarks'][0]['nose']['right_wing']['y']
    noseUpper_x = rinj['landmarks'][0]['nose']['right_wing']['x']
    lipTop_x = rinj['landmarks'][0]['mouth']['top']['x']
    lipTop_y = rinj['landmarks'][0]['mouth']['top']['y']
    lipBot_x = rinj['landmarks'][0]['mouth']['bottom']['x']
    lipBot_y = rinj['landmarks'][0]['mouth']['bottom']['y']
    lipRight_x = rinj['landmarks'][0]['mouth']['right_corner']['x']
    lipRight_y = rinj['landmarks'][0]['mouth']['right_corner']['y']
    lipCenter_y = (lipTop_y + lipBot_y) / 2
    lipCenter_x = (lipTop_x + lipBot_x) / 2
    faceLeftEdge_x = rinj['landmarks'][0]['face_contour']['point14']['x']
    faceRightEdge_x = rinj['landmarks'][0]['face_contour']['point15']['x']
    faceRightEdge_y = rinj['landmarks'][0]['face_contour']['point15']['y']
    faceMiddle_x = rinj['landmarks'][0]['nose']['tip']['x']
    faceBottom_y = rinj['landmarks'][0]['chin']['bottom']['y']

    #vertical: pupil to middle of mouth / middle of mouth to bottom of chin
    def ratio_v1():
        p1 = abs(iCenter_y - lipCenter_y)
        p2 = abs(lipCenter_y - faceBottom_y)
        return p1/p2

    #vertical: pupil to edge of nose / edge of nose to bottom of chin
    def ratio_v2():
        p1 = abs(iCenter_y - noseUpper_y)
        p2 = abs(noseUpper_y - faceBottom_y)
        return p1/p2

    #vertical: middle of eyebrow to upper eye / upper eye to lower eye
    def ratio_v4():
        p1 = abs(iBrow_y-iUpper_y)
        p2 = abs(iUpper_y-iLower_y)
        return p1/p2

    # pupil to edge of nose / edge of nose to middle of mouth
    def ratio_v5():
        p1 = math.dist((iCenter_x,iCenter_y),(noseUpper_x,noseUpper_y))
        p2 = math.dist((noseUpper_x,noseUpper_y),(lipCenter_x,lipCenter_y))
        return p1/p2

    # nose to top of lip / top of lip to lip corner
    def ratio_v7():
        p1 = math.dist((noseUpper_x,noseUpper_y),(lipTop_x,lipTop_y))
        p2 = math.dist((lipTop_x,lipTop_y),(lipRight_x,lipRight_y))
        return p1/p2

    #horizontal: edge of face to inner corner of near eye/ inner corner of near eye to edge of face on the far side
    def ratio_h1():
        p1 = abs(faceRightEdge_x - iLeft_x)
        p2 = abs(iLeft_x - faceLeftEdge_x)
        return p1/p2

    #horizontal ratio: middle of face to edge of eye / edge of eye to side of face
    def ratio_h3():
        p1 = abs(faceMiddle_x - iRight_x)
        p2 = abs(iRight_x - faceRightEdge_x)
        return p1/p2

    #horizontal ratio: edge of face to outer corner of eye/outer corner of eye to inner corner of eye
    def ratio_h4():
        p1 = abs(faceRightEdge_x-iRight_x)
        p2 = abs(iRight_x-iLeft_x)
        return p1/p2

    #horizontal: edge of face to outer eyebrow / outer eyebrow to outer edge of eye
    def ratio_h5():
        p1 = abs(faceRightEdge_x - iBrowRight_x)
        p2 = abs(iBrowRight_x - iRight_x)
        return p1/p2

    #horizontal ratio: tip of nose to edge of nose / edge of nose to coner of mouth
    def ratio_h6():
        p1 = abs(faceMiddle_x - noseUpper_x)
        p2 = abs(noseUpper_x-lipRight_x)
        return p1/p2
    #output a dictionary of ratios
    result = {}
    result["ratio_v1"] = ratio_v1()
    result["ratio_v2"] = ratio_v2()
    result["ratio_v4"] = ratio_v4()
    result["ratio_v5"] = ratio_v5()
    result["ratio_v7"] = ratio_v7()
    result["ratio_h1"] = ratio_h1()
    result["ratio_h3"] = ratio_h3()
    result["ratio_h4"] = ratio_h4()
    result["ratio_h5"] = ratio_h5()
    result["ratio_h6"] = ratio_h6()

    return result

#print(getRatios())

'''
    print("the ratio of v1 is {}.".format(ratio_v1()))
    print("the ratio of v2 is {}.".format(ratio_v2()))
    print("the ratio of v4 is {}.".format(ratio_v4()))
    print("the ratio of v5 is {}.".format(ratio_v5()))
    print("the ratio of v7 is {}.".format(ratio_v7()))
    print("the ratio of h1 is {}.".format(ratio_h1()))
    print("the ratio of h3 is {}.".format(ratio_h3()))
    print("the ratio of h4 is {}.".format(ratio_h4()))
    print("the ratio of h5 is {}.".format(ratio_h5()))
    print("the ratio of h6 is {}.".format(ratio_h6()))
    
    
    #print("The difference between eyebrow and eye's upper line is {}.".format(eyeUpper_y - iBrow_y))
    
    #print((rinj['landmarks'][0]['right_eye']))
    #print(eval((eval(response.content)['landmarks'])))
    #print(eval(response.text))
    #print(type(eval(response.content)['landmarks']))sud
    
'''