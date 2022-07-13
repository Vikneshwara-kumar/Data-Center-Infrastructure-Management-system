(define 
(domain DCIMS)

(:requirements  [:adl][:strips][:typing])



(:predicates    
                (Temp_HumidityOkay ?x )
                (SmokeDetectorOkay ?x )
                (MotionSnsrOkay ?x )
                (Servo_on ?x)
                (Alarm_on ?x )
              
)


(:action Fan
		:parameters  (?from ?to)
		:precondition (and  (Temp_HumidityOkay ?from))
		:effect (and  (Temp_HumidityOkay ?to) (not (Temp_HumidityOkay ?from))))

(:action Alarm 
    :parameters     (?x)
    :precondition   (and (not(SmokeDetectorOkay ?x)))
    :effect         (Servo_on ?x  ) 
)

(:action Motion_Detection 
    :parameters     ( ?x)
    :precondition   (and  (not (MotionSnsrOkay ?x)) )
    :effect         (Alarm_on ?x)   
)


)
