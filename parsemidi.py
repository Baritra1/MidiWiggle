import mido
import math
import csv

def midi_note_to_freq(note):
    return 440.0 * (2 ** ((note - 69) / 12))

def parse_midi(filename, csv_out="notes.csv"):
    mid = mido.MidiFile(filename)

    track_times = [0] * len(mid.tracks)

    events = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            track_times[i] += msg.time
            if msg.type in ('note_on', 'note_off', 'set_tempo'):
                events.append((track_times[i], msg))

    events.sort(key=lambda e: e[0])

    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # praying its 120 bpm

    def ticks_to_seconds(ticks):
        return mido.tick2second(ticks, ticks_per_beat, tempo)


    result = []
    active_note = None
    active_time = None

    for abs_tick, msg in events:
        if msg.type == 'set_tempo':
            tempo = msg.tempo  # update tempo if file changes it
        elif msg.type == 'note_on' and msg.velocity > 0:
            active_note = msg.note
            active_time = ticks_to_seconds(abs_tick)
        elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
            if active_note is not None:
                start_sec = active_time
                end_sec = ticks_to_seconds(abs_tick)
                duration = end_sec - start_sec
                freq = midi_note_to_freq(active_note)
                result.append((start_sec, duration, freq))
                active_note = None
                active_time = None

    with open(csv_out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["StartTime(s)", "Duration(s)", "Frequency(Hz)"])
        for row in result:
            writer.writerow(row)

    return result

notes = parse_midi("C:/Users/Aritra/Documents/CMU/16223/Blues10.mid", "drumnotes.csv")
