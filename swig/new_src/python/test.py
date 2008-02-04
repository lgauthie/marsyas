#!/usr/bin/env python

from marsyas import MarSystemManager,MarControlPtr

msm = MarSystemManager()

file = msm.create("SoundFileSource","file")
sink = msm.create("AudioSink","sink")
gain = msm.create("Gain", "gain")
pipe = msm.create("Series","pipe")

pipe.addMarSystem(file)
pipe.addMarSystem(gain)
pipe.addMarSystem(sink)

filename = pipe.getControl("SoundFileSource/file/mrs_string/filename")
notempty = pipe.getControl("SoundFileSource/file/mrs_bool/notEmpty")
iniAudio = pipe.getControl("AudioSink/sink/mrs_bool/initAudio")

filename.setValue_string("test.ogg")
iniAudio.setValue_bool(1)

while notempty.to_bool():
	pipe.tick()