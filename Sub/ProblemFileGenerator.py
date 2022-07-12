import requests
import sys

TempSensor = "off"
MotionSensor = False
SmokeSensor = False


def GenerateProblemPDDLFile(MotionSensor, SmokeSensor, TempSensor):
    global Fan, Serv , Alrm
    ProbFile = open("/home/pi/DCIMS-IoT/AI_Planning/Problem_File/DCIMS_ProblemFile.pddl","w+")
    ProbFile.write(
        "(define\n\n(problem DCIMS_action)\n\n(:domain DCIMS)\n\n(:objects\tLow Medium High off on prev not_optimum optimum\n)\n\n")
    ProbFile.write(
        "(:init\t")
    print(TempSensor)
    if (TempSensor == "Low"):
        ProbFile.write("\t(Temp_HumidityOkay prev)\n")
        Fan = "Temp_HumidityOkay Low"
    elif (TempSensor == "Medium"):
        ProbFile.write("\t\t(Temp_HumidityOkay prev)\n")
        Fan = "Temp_HumidityOkay Medium"
    elif (TempSensor == "High"):
        ProbFile.write("\t\t(Temp_HumidityOkay prev)\n")
        Fan = "Temp_HumidityOkay High"
    elif (TempSensor == "off"):
        ProbFile.write("(Temp_HumidityOkay prev)\n")
        Fan = "Temp_HumidityOkay off"

    if (SmokeSensor == True):
        ProbFile.write("\t\t(SmokeDetectorOkay optimum)\n")
        Serv = "Servo_on on"
    else:
        ProbFile.write("\t\t(SmokeDetectorOkay not_optimum)\n")
        Serv = "Servo_on off"
    if (MotionSensor == True):
        ProbFile.write("\t\t(MotionSnsrOkay optimum)\n")
        Alrm = "Alarm_on on"
    else:
        ProbFile.write("\t\t(MotionSnsrOkay not_optimum)\n")
        Alrm = "Alarm_on off"

    s1 = "(:goal\t(and ("
    s2 =  ")("
    s3 = ")("
    s4 = ") )\n) \n\n)"

    goal = s1+ Fan + s2 + Serv + s3 +Alrm +s4
    ProbFile.write(")\n\n")
    ProbFile.write(goal)

def GetAIPlan():
    data = {'domain': open(
        "/home/pi/DCIMS-IoT/AI_Planning/Domain_FIle/DCIMS_DomainFile.pddl",'r').read(),
            'problem': open(
                "/home/pi/DCIMS-IoT/AI_Planning/Problem_File/DCIMS_ProblemFile.pddl",
                'r').read()}

    response = requests.post('http://solver.planning.domains/solve', json=data).json()

    with open(
            "/home/pi/DCIMS-IoT/AI_Planning/AI_Plan/AIPlan.txt",
            'w') as f:
        for act in response['result']['plan']:
            f.write(str(act['name']))
            f.write('\n')

GenerateProblemPDDLFile(MotionSensor, SmokeSensor, TempSensor)
GetAIPlan()
