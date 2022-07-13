(define

(problem DCIMS_action)

(:domain DCIMS)

(:objects	Low Medium High off on prev not_optimum optimum
)

(:init		(Temp_HumidityOkay prev)
		(SmokeDetectorOkay not_optimum)
		(MotionSnsrOkay not_optimum)
)

(:goal	(and (Temp_HumidityOkay Low)(Servo_on off)(Alarm_on off) )
) 

)