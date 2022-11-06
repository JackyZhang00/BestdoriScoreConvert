import Note
class BPM(Note):
    '''
    BPM标识
    '''
    def __init__(self,bpm):
        self.beat = bpm
    def add(self):
        global beat
        ret = '{"type":"BPM","bpm":'+self.bpm+',"beat":'+str(beat)+'}'
        return ret