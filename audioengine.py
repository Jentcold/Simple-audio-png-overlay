from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

def get_session(name):
    sessions = AudioUtilities.GetAllSessions()
    sessions = [s for s in sessions if s.Process and s.Process.name() == name]
    session = sessions[0]
    if len(sessions) > 1:
        session = sessions[1]
    return session

def talk_check(session):
    peak = 0.00000
    meter = session._ctl.QueryInterface(IAudioMeterInformation)
    peak = max(peak, meter.GetPeakValue())
    print(f"{peak:.5f}",end='\r')
    return float(f"{peak:.5f}")
